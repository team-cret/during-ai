from transformers import pipeline

class BartLargeMnli:
    def __init__(self, sentiments, model_name) -> None:
        self.sentiments = sentiments
        self.classifier = pipeline(
            model=model_name,
            device_map='auto',
        )

    def classify_text(self, message:str) -> tuple[str, str]:
        result = self.classifier(
            message,
            candidate_labels=self.sentiments,
            multi_label=True
        )
        
        return {
            'sentiments' : result['labels'],
            'scores' : result['scores']
        }
