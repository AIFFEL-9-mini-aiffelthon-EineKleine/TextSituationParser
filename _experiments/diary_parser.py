import re
import json
import google.generativeai as genai

# Load/Use the custom environment variable
from dotenv import load_dotenv
from os import environ

load_dotenv()  # load the `.env` file -- 없다면 만들어야 합니다. 그리고 안에 `GEMINI_API_KEY="..."`와 같이 작성해주세요.

class TextSituationParser:
    def __init__(self, api_key):
        # Google Generative AI 설정
        self.api_key = environ.get('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.system_instruction = (
            'JSON schema로 상황을 나눠줘 너무 세분화 하지는 말고 큰 주제에 대해서 나눠줘, 상황을 나눌때는 원래 문장을 그대로 수정없이 놔둬줘, 상황은 1개이상으로 만들어줘:{{"상황1": <첫번째 상황의 원문>, "상황2": <두번째 상황의 원문>}}'
        )
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=self.system_instruction,
            generation_config={"response_mime_type": "application/json"}
        )
        self.chat_session = self.model.start_chat(history=[])
        
    @staticmethod
    def preprocess(text):
        # 공백 및 문장 부호 제거
        return re.sub(r'\s+|[^\w]', '', text)

    def calculate_mismatch_ratio(self, str1, str2):
        # 원문 복원률 계산
        str1 = self.preprocess(str1)
        str2 = self.preprocess(str2)
        min_length = min(len(str1), len(str2))
        mismatch_count = sum(str1[i] != str2[i] for i in range(min_length))
        mismatch_count += abs(len(str1) - len(str2))
        total_length = max(len(str1), len(str2))
        mismatch_ratio = 1 - mismatch_count / total_length
        return mismatch_ratio * 100

    def __call__(self, input_text):
        user_queries = [input_text, '다시 부탁할게 저번에 준 문장을 수정없이 그대로 상황에 대해서만 나눠줘']

        for user_query in user_queries:
            print(f'[사용자]: {user_query}')
            response = self.chat_session.send_message(user_query)
            answer_dict = json.loads(response.text)
            print(answer_dict)

            # 복원률 계산
            reconstruct_string = " ".join(answer_dict.values())
            recont_score = self.calculate_mismatch_ratio(reconstruct_string, input_text)
            print('원문 복원률 :', recont_score, '%')

            if recont_score > 90:
                return answer_dict
            else:
                print('[Error] : 상황 분류시 원문 정보 손실이 큼 다시 시도 중')

        return answer_dict  # 마지막 시도에서 반환된 answer_dict