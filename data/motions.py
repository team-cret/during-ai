
motions = {
    # solo motion
    1000 : {'motion' : '웃기'},
    1001 : {'motion' : '화내기'},
    1002 : {'motion' : '사랑해'},
    1003 : {'motion' : '부끄러움'},
    1004 : {'motion' : '응원하기'},
    1005 : {'motion' : '안아줘요'},
    1006 : {'motion' : '손 흔들기'},
    1007 : {'motion' : '피곤함'},

    # multi motion
    2000 : {'motion' : '포옹하기'},
    2001 : {'motion' : '뽀뽀하기'},
    2002 : {'motion' : '쓰다듬기'},

    # object motion
    3000 : {'motion' : '밥먹기'},
    3001 : {'motion' : '노트북하기'},
    3002 : {'motion' : '운동하기'},
    3003 : {'motion' : '잠자기'},
}

motion_to_id = {}
for key, value in motions.items():
    motion_to_id[value['motion']] = key