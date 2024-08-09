
sentiments = {
    0 : {'sentiment' : '웃기'},
    1 : {'sentiment' : '화내기'},
    2 : {'sentiment' : '사랑해'},
    3 : {'sentiment' : '부끄러움'},
    4 : {'sentiment' : '응원하기'},
    5 : {'sentiment' : '안아줘요'},
    6 : {'sentiment' : '손 흔들기'},
    7 : {'sentiment' : '피곤함'},
    8 : {'sentiment' : '포옹하기'},
    9 : {'sentiment' : '뽀뽀하기'},
    10: {'sentiment' : '쓰다듬기'},
}

sentiment_to_id = {}
for key, value in sentiments.items():
    sentiment_to_id[value['sentiment']] = key