from collections import Counter

from data.motion_keyword import matched_keywords
from data.motions import motion_to_id
from model.data_model import Motion

class KeywordAnalyzer:
    def __init__(self) -> None:
        self.set_keyword_dictionary()

    # chat <-> keyword matching
    def is_keyword(self, text:str) -> Motion:
        if text in self.keyword_dictionary:
            return Motion(
                motion=self.keyword_dictionary[text],
                motion_id=motion_to_id[self.keyword_dictionary[text]],
            )
        
        if Counter(text)['ㅋ'] * 3 >= len(text):
            return Motion(
                motion='웃기',
                motion_id=1000,
            )
        return False
    
    def set_keyword_dictionary(self) -> None:
        self.keyword_dictionary = {}

        for motion in list(matched_keywords.keys()):
            for keyword in matched_keywords[motion]:
                self.keyword_dictionary[keyword] = motion