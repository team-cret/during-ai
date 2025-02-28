
motions = {
    # solo motion
    1000 : {'motion' : '웃기', 'key': 'laugh'},
    1001 : {'motion' : '화내기', 'key': 'angry'},
    1002 : {'motion' : '사랑해', 'key': 'love-you'},
    1003 : {'motion' : '부끄러움', 'key': 'shy'},
    1004 : {'motion' : '응원하기', 'key': 'cheer-up'},
    1005 : {'motion' : '안아줘요', 'key': 'hug-me'},
    1006 : {'motion' : '손 흔들기', 'key': 'waving'},
    1007 : {'motion' : '피곤함', 'key': 'tired'},

    # multi motion
    2000 : {'motion' : '포옹하기', 'key': 'hug'},
    2001 : {'motion' : '뽀뽀하기', 'key': 'kiss'},
    2002 : {'motion' : '쓰다듬기', 'key': 'pat'},

    # object motion
    3000 : {'motion' : '밥먹기', 'key': 'eat'},
    3001 : {'motion' : '공부하기', 'key': 'study'},
    3002 : {'motion' : '운동하기', 'key': 'exercise'},
    3003 : {'motion' : '잠자기', 'key': 'sleep'},

    # none motion
    9999 : {'motion' : '없음', 'key':'none'}
}

motion_to_id = {}
for key, value in motions.items():
    motion_to_id[value['motion']] = key