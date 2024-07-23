from transformers import pipeline

class HuggingfaceFacebookBartLargeMnliAnalyzer:
    def __init__(self, sentiments) -> None:
        self.sentiments = sentiments
        self.threshold = 0.5
        self.classifier = pipeline(
            model='facebook/bart-large-mnli',
            device_map='auto',
        )

    def analyzeSentimentByChat(self, chatData):
        result = self.classifier(
            chatData,
            candidate_labels=self.sentiments,
            multi_label=True
        )

        if result['scores'][0] > self.threshold:
            return (result['labels'][0], result['scores'][0])
        return ('없음', -1)

# Model 동작 확인 O
# model = HuggingfaceFacebookBartLargeMnliAnalyzer()
# print(model.analyzeSentimentByChat(['positive', 'negative'], 'I love you'))