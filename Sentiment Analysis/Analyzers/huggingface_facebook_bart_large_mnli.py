from transformers import pipeline

class HuggingfaceFacebookBartLargeMnliAnalyzer:
    def __init__(self) -> None:
        self.classifier = pipeline(
            model='facebook/bart-large-mnli',
            device_map='auto',
        )

    def analyzeSentimentByChat(self, sentiments, chatData):
        result = self.classifier(
            chatData,
            candidate_labels=sentiments,
            multi_label=True
        )

        if result['scores'][0] > 0.5:
            return [result['labels'][0], result['scores'][0]]
        return ['없음', -1]

# Model 동작 확인 O
# model = HuggingfaceFacebookBartLargeMnliAnalyzer()
# print(model.analyzeSentimentByChat(['positive', 'negative'], 'I love you'))