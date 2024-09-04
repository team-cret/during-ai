from collections import Counter
from tqdm import tqdm

from ai_model.classification.pogjin_roberta import PongjinRobertaTextClassification
from model.data_model import Report, CoupleChat
    
class AIAnalyzer:
    def __init__(self):
        self.ai_report:Report = Report()

    def analyze_by_ai(self, couple_chat:list[CoupleChat]):
        self.couple_chat = couple_chat
        self.analyze_mbti()
        self.analyze_frequently_talked_topic()
        self.analyze_frequency_of_affection()
        self.analyze_sweetness_score()

        return self.ai_report

    def analyze_mbti(self):
        pass

    def analyze_frequently_talked_topic(self):
        pass

    def analyze_frequency_of_affection(self):
        ai_classifier = PongjinRobertaTextClassification()

        tf_affection = ai_classifier.is_affection_batch_classification(
            [chat.message for chat in self.couple_chat[:500]]
        )

        time_period = self.couple_chat[-1].timestamp - self.couple_chat[0].timestamp
        self.ai_report.frequency_of_affection = time_period / (Counter(tf_affection)[True] * len(self.couple_chat) / 500)
    
    def analyze_sweetness_score(self):
        pass