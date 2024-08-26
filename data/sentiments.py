
sentiments = {
    # solo interaction
    1000 : {'sentiment' : '웃기'},
    1001 : {'sentiment' : '화내기'},
    1002 : {'sentiment' : '사랑해'},
    1003 : {'sentiment' : '부끄러움'},
    1004 : {'sentiment' : '응원하기'},
    1005 : {'sentiment' : '안아줘요'},
    1006 : {'sentiment' : '손 흔들기'},
    1007 : {'sentiment' : '피곤함'},

    # multi interaction
    2000 : {'sentiment' : '포옹하기'},
    2001 : {'sentiment' : '뽀뽀하기'},
    2002 : {'sentiment' : '쓰다듬기'},

    # object interaction
    3000 : {'sentiment' : '밥먹기'},
    3001 : {'sentiment' : '노트북하기'},
    3002 : {'sentiment' : '운동하기'},
    3003 : {'sentiment' : '잠자기'},
}

sentiment_to_id = {}
for key, value in sentiments.items():
    sentiment_to_id[value['sentiment']] = key