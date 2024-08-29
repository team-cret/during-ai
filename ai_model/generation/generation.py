from abc import ABC, abstractmethod
from typing import List, Dict

from model.data_model import CoupleChat, Motion

class Generation(ABC):
    @abstractmethod
    def set_model(self) -> None:
        pass

    @abstractmethod
    def generate_text(self, user_prompt: str, history: List[Dict], system_prompt: str) -> str:
        pass

    @abstractmethod
    def generate_text_chat_mode(self, user_prompt: str, history: List[Dict], system_prompt: str, is_stream: bool = False) -> str:
        pass

    @abstractmethod
    def analyze_motion(self, chat: CoupleChat) -> Motion:
        pass
