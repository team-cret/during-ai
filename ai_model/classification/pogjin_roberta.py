from abc import ABC, abstractmethod
import logging
from concurrent.futures import ProcessPoolExecutor

from transformers import pipeline

from ai_model.classification.text_classification import TextClassification
from data.motions import motions
from setting.logger_setting import logger_setting
from setting.model_config import ModelConfig

class PongjinRobertaTextClassification(TextClassification):
    def __init__(self) -> None:
        self.set_model()
        self.set_logger()
    
    def set_logger(self) -> None:
        logger_setting()
        self.logger = logging.getLogger(__name__)

    def set_model(self) -> None:
        self.motions = [value['motion'] for value in motions.values()]
        
        self.classifier = pipeline(
            'zero-shot-classification',
            args_parser=CustomZeroShotClassificationArgumentHandler(),
            model=ModelConfig.PONGJIN_ROBERTA_CLASSIFICATION_MODEL.value,
            device=ModelConfig.CLASSIFICATION_MODEL_DEVICE.value,
        )

        self.classifiers = [
            pipeline(
                'zero-shot-classification',
                args_parser=CustomZeroShotClassificationArgumentHandler(),
                model=ModelConfig.PONGJIN_ROBERTA_CLASSIFICATION_MODEL.value,
                device=ModelConfig.CLASSIFICATION_MODEL_DEVICE.value,
            ) for _ in range(3)
        ]

    def classify_text(self, text:str) -> dict:
        try:
            result = self.classifier(
                text,
                    candidate_labels=self.motions,
                hypothesis_template="이 문장에서 느껴지는 감정은 {}이다.",
            )

            return {
                'motions' : result['labels'],
                'scores' : result['scores']
            }
        except Exception as e:
            self.logger.error(f"classification model error: {str(e)}")
            return {
                'motions' : [],
                'scores' : []
            }
    
    def classify_text_by_hypothesis(self, text:str, hypothesis:str, labels:list[str]) -> dict:
        try:
            result = self.classifier(
                text,
                candidate_labels=labels,
                hypothesis_template=hypothesis,
            )

            return {
                'labels' : result['labels'],
                'scores' : result['scores']
            }
        except Exception as e:
            self.logger.error(f"classification model error: {str(e)}")
            return {
                'motions' : [],
                'scores' : []
            }

    def is_affection(self, text:str) -> bool:
        result = self.classifier(
            text,
            candidate_labels=['사랑표현 이', '사랑표현이 아니'],
            hypothesis_template="이 문장은 {}다.",
        )

        return result['labels'][0] == '사랑표현 이'
    
    def is_affection_batch_classification(self, texts:list[str]) -> list[bool]:
        results = self.classifier(
            texts,
            candidate_labels=['사랑표현 이', '사랑표현이 아니'],
            hypothesis_template="이 문장은 {}다.",
        )

        return [result['labels'][0] == '사랑표현 이' for result in results]

class ArgumentHandler(ABC):
    """
    Base interface for handling arguments for each :class:`~transformers.pipelines.Pipeline`.
    """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class CustomZeroShotClassificationArgumentHandler(ArgumentHandler):
    """
    Handles arguments for zero-shot for text classification by turning each possible label into an NLI
    premise/hypothesis pair.
    """

    def _parse_labels(self, labels):
        if isinstance(labels, str):
            labels = [label.strip() for label in labels.split(",")]
        return labels

    def __call__(self, sequences, labels, hypothesis_template):
        if len(labels) == 0 or len(sequences) == 0:
            raise ValueError("You must include at least one label and at least one sequence.")
        if hypothesis_template.format(labels[0]) == hypothesis_template:
            raise ValueError(
                (
                    'The provided hypothesis_template "{}" was not able to be formatted with the target labels. '
                    "Make sure the passed template includes formatting syntax such as {{}} where the label should go."
                ).format(hypothesis_template)
            )

        if isinstance(sequences, str):
            sequences = [sequences]
        labels = self._parse_labels(labels)

        sequence_pairs = []
        for label in labels:
            # 수정부: 두 문장을 페어로 입력했을 때, `token_type_ids`가 자동으로 붙는 문제를 방지하기 위해 미리 두 문장을 `sep_token` 기준으로 이어주도록 함
            sequence_pairs.append(f"{sequences} {hypothesis_template.format(label)}")

        return sequence_pairs, sequences
