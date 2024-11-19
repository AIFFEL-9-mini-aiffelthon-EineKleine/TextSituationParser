from transformers import pipeline
import pytextrank
import spacy


class DiarySenAnaly:
    def __init__(self, input_text):
        self.input_text = input_text

    def split_sentence(self):
        """Splits the input text into sentences."""
        self.seper_senten = self.input_text.split('.')
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
    def filter_sementic(self, result):
        """Filters sentences based on important emotion labels and combines them with previous sentences."""
        important_labels = {"😱", "😲", "😡", "😢", "😊", "🤢","🤔"}  # Labels of interest
        filter_seper_senten = [self.seper_senten[i] for i, label in enumerate(result) if label in important_labels]
        filter_seper_label = [result[i] for i, label in enumerate(result) if label in important_labels]

        # Combine each selected sentence with the previous one
        filter_seper_senten2 = []
        for i in range(len(filter_seper_senten)):
            index = self.seper_senten.index(filter_seper_senten[i])
            if index > 0:
                combined_sentence = self.seper_senten[index - 1] + ' ' + filter_seper_senten[i]
                filter_seper_senten2.append(combined_sentence)
            else:
                filter_seper_senten2.append(filter_seper_senten[i])

        return filter_seper_senten, filter_seper_label
    
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

    def __call__(self):
        """Runs the full analysis when the class is called."""
        # Split sentences
        self.split_sentence()

        # Perform semantic classification
        emotion_analyzer = self.create_emotion_analyzer()
        result_s_model = self.analyze_diary_entry(self.seper_senten, emotion_analyzer)

        # Filter sentences
        filter_seper_senten, filter_seper_label = self.filter_sementic(result_s_model)

        # Extract keywords
        result_k_model = self.keyword_extract_f(filter_seper_senten)

        # Output results
        print("Separated Sentences:", self.seper_senten)
        print("sentic classific per sentence:", result_s_model)
        print("Filtered Sentences:", filter_seper_senten)
        print("Filtered sentiment:", filter_seper_label)
        print("Keywords:", result_k_model)
        return filter_seper_senten, filter_seper_label, result_k_model