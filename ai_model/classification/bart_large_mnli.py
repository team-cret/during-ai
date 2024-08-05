from transformers import pipeline

class BartLargeMnli:
    def __init__(self, sentiments, model_name, threshold) -> None:
        self.threshold = threshold
        self.sentiments = sentiments
        self.classifier = pipeline(
            model=model_name,
            device_map='auto',
        )

    def analyze_message(self, message:str) -> tuple[str, str]:
        result = self.classifier(
            message,
            candidate_labels=self.sentiments,
            multi_label=True
        )

        if result['scores'][0] > self.threshold:
            return (result['labels'][0], result['scores'][0])
        return ('없음', -1)
