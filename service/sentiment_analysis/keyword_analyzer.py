from data import sentiment_keyword

class KeywordAnalyzer:
    def __init__(self) -> None:
        self.matched_keywords = sentiment_keyword.matched_keywords
        self.set_keyword_dictionary()

    def is_keyword(self, text:str) -> dict['sentiment':str, 'sentiment_id':int]:
        if text in self.keyword_dictionary:
            return self.keyword_dictionary[text]
        return False
    
    def set_keyword_dictionary(self) -> None:
        self.keyword_dictionary = {}

        for sentiment in list(self.matched_keywords.keys()):
            for keyword in self.matched_keywords[sentiment]:
                self.keyword_dictionary[keyword] = sentiment
