# test type
# 0 : general
# 1 : mixed
# 2 : cuty tone
# 3 : space, punctuation
# 4 : honofic
# 5 : difficult

data = [
    # solo interaction
    # 1000 : {'sentiment' : '웃기'},
    {'contents_type' : 'text', 'label' : '웃기', 'type': 0, 'content' : 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ'},
    # 1001 : {'sentiment' : '화내기'},
    {'contents_type' : 'text', 'label' : '화내기', 'type': 0, 'content' : '화낼거야'},
    # 1002 : {'sentiment' : '사랑해'},
    {'contents_type' : 'text', 'label' : '사랑해', 'type' : 0, 'content' : '사랑해'},
    {'contents_type' : 'text', 'label' : '사랑해', 'type' : 3, 'content' : '사랑해요'},
    {'contents_type' : 'text', 'label' : '사랑해', 'type' : 2, 'content' : '사댱행'},
    {'contents_type' : 'text', 'label' : '사랑해', 'type' : 2, 'content' : '사댱해'},
    {'contents_type' : 'text', 'label' : '사랑해', 'type' : 1, 'content' : '사댱해요'},
    # 1003 : {'sentiment' : '부끄러움'},
    # 1004 : {'sentiment' : '응원하기'},
    {'contents_type' : 'text', 'label' : '응원하기', 'type' : 3, 'content' : '오늘도 화이팅 하고 와요!'},
    {'contents_type' : 'text', 'label' : '응원하기', 'type' : 1, 'content' : '오늘도 화이팅 하구 와요!'},
    {'contents_type' : 'text', 'label' : '응원하기', 'type' : 3, 'content' : '오늘도 잘 하고 와요!'},
    {'contents_type' : 'text', 'label' : '응원하기', 'type' : 0, 'content' : '오늘도 잘 하고와'},
    {'contents_type' : 'text', 'label' : '응원하기', 'type' : 0, 'content' : '잘 하고와'},
    # 1005 : {'sentiment' : '안아줘요'},
    # 1006 : {'sentiment' : '손 흔들기'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 0, 'content' : '안녕'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 2, 'content' : '안뇽'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 2, 'content' : '안냥'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 0, 'content' : '좋은아침'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 3, 'content' : '좋은아침!'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 4, 'content' : '잘자요'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 1, 'content' : '잘자요~'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 3, 'content' : '잘 자요'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 3, 'content' : '잘 자요~'},
    {'contents_type' : 'text',  'label' : '손 흔들기', 'type' : 3, 'content' : '잘 자요~!'},
    # 1007 : {'sentiment' : '피곤함'},
    {'contents_type' : 'text', 'label' : '피곤함', 'type' : 0, 'content' : '오늘은 너무 피곤해'},
    {'contents_type' : 'text', 'label' : '피곤함', 'type' : 0, 'content' : '오늘은 좀 힘드네'},
    {'contents_type' : 'text', 'label' : '피곤함', 'type' : 0, 'content' : '오늘은 쉬고싶어'},
    {'contents_type' : 'text', 'label' : '피곤함', 'type' : 0, 'content' : '쉬고싶어'},

    # # multi interaction
    # 2000 : {'sentiment' : '포옹하기'},
    # 2001 : {'sentiment' : '뽀뽀하기'},
    # 2002 : {'sentiment' : '쓰다듬기'},
    {'contents_type' : 'text', 'label' : '쓰다듬기', 'type' : 0, 'content' : '오늘도 고생했어'},
    {'contents_type' : 'text', 'label' : '쓰다듬기', 'type' : 2, 'content' : '오늘도 고생했져'},

    # # object interaction
    # 3000 : {'sentiment' : '밥먹기'},
    {'contents_type' : 'text', 'label' : '밥먹기', 'type' : 0, 'content' : '밥 먹고 올게'},
    {'contents_type' : 'text', 'label' : '밥먹기', 'type' : 2, 'content' : '밥 먹구 올게'},
    {'contents_type' : 'text', 'label' : '밥먹기', 'type' : 1, 'content' : '밥 먹구 올게요'},
    {'contents_type' : 'text', 'label' : '밥먹기', 'type' : 4, 'content' : '밥 먹고 올게요'},
    {'contents_type' : 'text', 'label' : '밥먹기', 'type' : 1, 'content' : '밥 머꾸 올게요'},
    {'contents_type' : 'text', 'label' : '밥먹기', 'type' : 2, 'content' : '밥 머꾸 오꼐'},
    # 3001 : {'sentiment' : '노트북하기'},
    {'contents_type' : 'text', 'label' : '노트북하기', 'type' : 0, 'content' : '공부하고 있어'},
    # 3002 : {'sentiment' : '운동하기'},
    # 3003 : {'sentiment' : '잠자기'},

    # None
    {'contents_type' : 'text', 'label' : '없음', 'type' : 3, 'content' : '오늘은 뭐해?'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 0, 'content' : '귀여워'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 0, 'content' : '알았어'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 3, 'content' : '퇴근했어!'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 0, 'content' : '퇴근'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 3, 'content' : '퇴근!'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 2, 'content' : '힣'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 2, 'content' : '헿'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 2, 'content' : '잉'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 2, 'content' : '밍구'},
    {'contents_type' : 'text', 'label' : '없음', 'type' : 5, 'content' : '나 요즘 너무 힘들어서 디올 가방 샀어'},
    
]