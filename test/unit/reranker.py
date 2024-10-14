
from model.data_model import RetrievedData
from ai_model.reranker.bge_reranker_v2_m3 import BgeRerankerV2M3

class RerankerTester:
    def __init__(self) -> None:
        self.model = BgeRerankerV2M3()
        self.setup_for_test()

    def setup_for_test(self):
        self.test_message = [
            RetrievedData(
                original_message='안녕하세요',
            ),
            RetrievedData(
                original_message='반가워요',
            ),
            RetrievedData(
                original_message='고마워요',
            ),
            RetrievedData(
                original_message='잘가요',
            ),
        ]

    def test(self):
        print(self.model.rerank_documents(self.test_message, '안녕하세요'))