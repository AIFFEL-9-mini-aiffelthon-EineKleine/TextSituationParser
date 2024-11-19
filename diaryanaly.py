class DiarySenAnaly:
    def __init__(self, input_text):
        self.input_text = input_text

    def split_sentence(self):
        """Splits the input text into sentences."""
        self.seper_senten = self.input_text.split('.')
        self.seper_senten = [sentence.strip() for sentence in self.seper_senten if sentence.strip()]
        return self.seper_senten
    
    ####################################
    ### 감정분류 모델 넣기#############
        # 감정 분석을 위한 Hugging Face 파이프라인 설정
    def create_emotion_analyzer(self):
        """Creates and returns a Hugging Face pipeline for emotion analysis using a Korean model."""
        return pipeline("text-classification", model="beomi/kcbert-base")

    def analyze_diary_entry(self, diary_entry, emotion_analyzer):
        """
        Analyzes the emotion of a diary entry using a given emotion analyzer pipeline.

        Parameters:
        diary_entry (str): The diary text to analyze.
        emotion_analyzer (Pipeline): The Hugging Face pipeline object for emotion analysis.

        Returns:
        dict: A dictionary containing the analyzed emotion and the corresponding emoji.
        """
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

        # 감정 분석 수행
        emotion_result = emotion_analyzer(diary_entry)[0]
        emotion = emotion_result["label"]
        emoji = emotion_to_emoji.get(emotion, "🤔")  # 매핑되지 않은 경우 기본 이모지 사용
        return {"emotion": emotion, "emoji": emoji}
    ################################
    def sementic_classfiy_f(self, sentences):
        """Dummy function for semantic classification."""
        return [1, 3, 4]  # Replace with your real classification logic
    ########################################


    ### 감정 분류시 중립 제외 인덱스로 수정 ##
    def filter_sementic(self, result):
        """Filters sentences based on important emotion labels and combines them with previous sentences."""
        important_labels = {4}  # Labels of interest
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

        return filter_seper_senten2, filter_seper_label
    

    ####################################
    ### 키워드 추출 모델 넣기#############
    ####################################
    def keyword_extract_f(self, sentences):
        """Dummy function for keyword extraction."""
        return ["keyword1", "keyword2"]  # Replace with your real keyword extraction logic
    ####################################


    def __call__(self):
        """Runs the full analysis when the class is called."""
        # Split sentences
        self.split_sentence()

        # Perform semantic classification
        result_s_model = self.sementic_classfiy_f(self.seper_senten)

        # Filter sentences
        filter_seper_senten, filter_seper_label = self.filter_sementic(result_s_model)

        # decoding label 2 sentic 'str'
        ## 숫자 라벨을 글자로 바꿔주는 코드 작성 
        # input  = filter_seper_label -> output = ['행복', '슬픔', '혐오']  등등

        # Extract keywords
        result_k_model = self.keyword_extract_f(filter_seper_senten)

        # Output results
        print("Separated Sentences:", self.seper_senten)
        print("sentic classific per sentence:", result_s_model)
        print("Filtered Sentences:", filter_seper_senten)
        print("Filtered sentiment:", filter_seper_label)
        print("Keywords:", result_k_model)
        return filter_seper_senten, filter_seper_label, result_k_model
