from .Analyzers.openai_embedding_model import OpenAIEmbeddingModel

class SentimentAnalyzerPreprocessor:
    def __init__(self) -> None:
        self.setSentiments()
        self.setEmbeddingModel()
        self.embeddingSentiments()
        pass

    def setSentiments(self):
        # 현재 MVP에 해당하는 감정 종류들
        self.sentiments = [
            '웃기', # 기쁨
            '화내기', # 화남
            '사랑해', # 사랑표현?
            '부끄러움', # 
            '응원하기', # 
            '안아줘요', # 힘듬, 우울함
            '손 흔들기', # 반가움, 
            '피곤함',
            '포옹하기', # 다녀올게
            '뽀뽀하기', # 뽀뽀
            '쓰다듬기', # 수고했어, 잘했어, 귀여워
        ]

        self.sentimentIds = {
            '웃기' : 0,
            '화내기' : 1,
            '사랑해' : 2,
            '부끄러움' : 3,
            '응원하기' : 4,
            '안아줘요' : 5,
            '손 흔들기': 6,
            '피곤함' : 7,
            '포옹하기' : 8,
            '뽀뽀하기' : 9,
            '쓰다듬기' : 10,
        }
    
    def setEmbeddingModel(self):
        # embeddingModel 이름
        self.embeddingModelNames = [
            'openai_embedding_model',
        ]

        # embeddingModel 이름 : Model객체
        # Model객체는 method 통일을 위해 각자의 파일에서 API화 되어 있음
        self.embeddingModels = {
            str(self.embeddingModelNames[0]) : OpenAIEmbeddingModel(0),
        }
    
    def embeddingSentiments(self):
        # 각 embeddingModel마다 embedding값 생성
        # embedding값은 Model마다 dictionary에 Model명을 통해서 관리
        self.embededValuesOfSentiments = {}
        for embeddingModelName in self.embeddingModelNames:
            embeddingModel = self.embeddingModels[embeddingModelName]

            # 각 감정별로 현재 모델로 Embedding값 생성
            self.embededValuesOfSentiments[embeddingModelName] = {}
            for sentiment in self.sentiments:
                embededVector = embeddingModel.getEmbeddingVector(sentiment)
                self.embededValuesOfSentiments[embeddingModelName][sentiment] = embededVector
