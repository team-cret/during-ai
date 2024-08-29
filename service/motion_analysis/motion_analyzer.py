from abc import ABC, abstractmethod

from model.data_model import CoupleChat, Motion

class MotionAnalyzer:
    @abstractmethod
    def analyze_motion(self, chat:CoupleChat) -> Motion:
        pass