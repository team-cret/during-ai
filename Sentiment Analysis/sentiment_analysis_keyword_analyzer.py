
class KeywordAnalyzer:
    def __init__(self, sentiments, sentimentIds) -> None:
        self.sentiments = sentiments
        self.sentimentIds = sentimentIds
        
        self.exactSentimentMatching()

    def analyzeSentimentByKeyword(self, chatData):
        if chatData in self.exactMatchingDictionary:
            return self.exactMatchingDictionary[chatData]
        return False
    
    def setExactMatchingDictionary(self):
        self.exactMatchingDictionary = {}
        matchedKeywords = {
            '웃기'     : [],
            '화내기'   : [],
            '사랑해'   : ['사랑해'],
            '부끄러움' : [],
            '응원하기' : ['화이팅'],
            '안아줘요' : [],
            '손 흔들기': ['안녕'],
            '피곤함'   : ['피곤해'],
            '포옹하기' : [],
            '뽀뽀하기' : ['뽀뽀'],
            '쓰다듬기' : [],
        }

        for sentiment in list(matchedKeywords.keys()):
            for keyword in matchedKeywords[sentiment]:
                self.exactMatchingDictionary[keyword] = sentiment
