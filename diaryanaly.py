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