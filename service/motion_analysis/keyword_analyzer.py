from data.motion_keyword import matched_keywords

class KeywordAnalyzer:
    def __init__(self) -> None:
        self.set_keyword_dictionary()

    # chat <-> keyword matching
    def is_keyword(self, text:str) -> dict['motion':str, 'motion_id':int]:
        if text in self.keyword_dictionary:
            return self.keyword_dictionary[text]
        return False
    
    def set_keyword_dictionary(self) -> None:
        self.keyword_dictionary = {}

        for motion in list(matched_keywords.keys()):
            for keyword in matched_keywords[motion]:
                self.keyword_dictionary[keyword] = motion