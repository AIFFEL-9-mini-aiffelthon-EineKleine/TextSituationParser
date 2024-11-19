from transformers import pipeline
import pytextrank
import spacy


class DiarySentimentAnalysis:
    def split_sentence(self, input_text: str):
        """Splits the input text into sentences."""
        self.seper_senten = input_text.split('.')
        self.seper_senten = [sentence.strip() for sentence in self.seper_senten if sentence.strip()]
        return self.seper_senten
    
    def create_emotion_analyzer(self):
        return pipeline("text-classification", model="beomi/kcbert-base")

    def analyze_diary_entry(self,sentences, emotion_analyzer):
        # 감정 -> 이모지 매핑
        emotion_to_emoji = {
            "공포": "😱",
            "놀람": "😲",
            "분노": "😡",
            "슬픔": "😢",
            "중립": "😐",
            "행복": "😊",
            "혐오": "🤢"
        }

        result = []
        for sentence in sentences:

            # 감정 분석 수행
            emotion_result = emotion_analyzer(sentence)[0]
            emotion = emotion_result["label"]
            emoji = emotion_to_emoji.get(emotion, "🤔")  # 매핑되지 않은 경우 기본 이모지 사용
            result.append(emoji)
        return result


    ### 감정 분류시 중립 제외 인덱스로 수정 ##
    def filter_sementic(self, result: list[str]):
        """Filters sentences based on important emotion labels and combines them with previous sentences."""
        important_labels = {"😱", "😲", "😡", "😢", "😊", "🤢","🤔"}  # Labels of interest
        filter_seper_senten = [self.seper_senten[i] for i, label in enumerate(result) if label in important_labels]
        filter_seper_label = [result[i] for i, label in enumerate(result) if label in important_labels]

        # Combine each selected sentence with the previous one
        filter_seper_senten2 = []
        for item in filter_seper_senten:
            index = self.seper_senten.index(item)
            if index > 0:
                combined_sentence = f'{self.seper_senten[index - 1]} {item}'
                filter_seper_senten2.append(combined_sentence)
            else:
                filter_seper_senten2.append(item)

        return filter_seper_senten, filter_seper_label
    
    def get_only_pred_labels_filterd(self, pred_result: list[str]) -> list[str]:
        a, filtered_pred_labels = self.filter_sementic(pred_result)
        return filtered_pred_labels
    
    def keyword_extract_f(self, sentences):
        keyword = []
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("textrank")

        for sentence in sentences:
            doc = nlp(sentence)
            keyword_sourece = [phrase.text for phrase in doc._.phrases[:1]]
            print()
            keyword.append(keyword_sourece)
        return keyword

    def __call__(self, input_text: str):
        """Runs the full analysis when the class is called."""
        # Split sentences
        self.split_sentence(input_text=input_text)

        # Perform semantic classification
        emotion_analyzer = self.create_emotion_analyzer()
        result_s_model = self.analyze_diary_entry(self.seper_senten, emotion_analyzer)

        # Filter sentences
        filter_seper_senten, pred_labels_filterd = self.filter_sementic(result_s_model)

        # Extract keywords
        result_k_model = self.keyword_extract_f(filter_seper_senten)

        # Output results
        print("Separated Sentences:", self.seper_senten)
        print("sentimental classificatioin per sentence:", result_s_model)
        print("Filtered Sentences:", filter_seper_senten)
        print("Filtered sentiment:", pred_labels_filterd)
        print("Keywords:", result_k_model)
        return filter_seper_senten, pred_labels_filterd, result_k_model
    
    
if __name__ == "__main__":
    from diaryanaly import DiarySentimentAnalysis
    diary_analyzer = DiarySentimentAnalysis()

    test_case_1 = "안녕하세요~ 오늘은 진짜 좋은일이있었습니다. 그런데 안좋은일도있었어요. 코드를 짜는데 집중이 하나도안되네.."
    test_case_2 = "오늘은 정신이 혼란스러운 하루였다. 생산직이나 알바, 무슨 일이든 하려는데 여러 직장에서의 전화로 정신없이 바쁜 하루를 보냈다. 물론 업무도 바빠서 승급 시험과 제출 기한이 코앞에 다가와 있어서 더욱 긴장되는 상황이었다. 늦잠을 자서 회사에 늦게 가야 했고, 친구의 클럽 모임 사실을 알게 되어 당황스러운 일도 있었다."
    
    test_case = test_case_2  # shadowing (act as a switch)
    
    filter_seper_senten, result_s_model, result_k_model = \
        diary_analyzer(test_case)
    
    custom_test_result = diary_analyzer.get_only_pred_labels_filterd(test_case)
    print(f"custom test result - {custom_test_result}")
# end main