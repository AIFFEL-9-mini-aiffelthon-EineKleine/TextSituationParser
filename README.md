# 모델 전체 프레임을 짠 코드입니다

```python
from diaryanaly import DiarySenAnaly

input_text = '안녕하세요~ 오늘은 진짜 좋은일이있었습니다. 그런데 안좋은일도있었어요. 코드를 짜는데 집중이 하나도안되네..'
diary_analyzer = DiarySenAnaly(input_text)
filter_seper_senten, result_s_model, result_k_model = diary_analyzer()
```

# 여기서는 안쓰이는 상황분류 모델 설명
# TextSituationParser
상황 분류 모델입니다

### 제미나이 사용을 하기위해 설치해주셔야합니다.
-  Levenshtein는 문장 두개 비교 계산기 입니다

```bash
pip install -r requirements.txt
```
위 명령을 통해 파이썬 패키지를 설치해야 합니다.  
그리고 `.env` 파일을 만들고 안에 다음과 같이 작성해주세요.

```bash
GEMINI_API_KEY="<API키>"
```

https://ai.google.dev/ <- 제미나이 API 발급 링크
### 안쪽에 API 키를 입력하는 란이있습니다.
```python
# diaryParset.py 파일 디렉토리를 같은곳에 두세요
from diaryParser import TextSituationParser

GOOGLE_API_KEY = 'your_API_key'
input_text = (
        '일기 텍스트 넣기'
    )

parser = TextSituationParser(api_key=GOOGLE_API_KEY)
answer_dict = parser(input_text)
print("결과 :", answer_dict)

```
