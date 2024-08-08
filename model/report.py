from datetime import datetime, timedelta
from pydantic import BaseModel
from setting.service_config import ServiceConfig

class Report(BaseModel):
    report_type:str = ''
    image:str = ''
    MBTI:str = ''
    response_time_zone: list = [0 for _ in range(round(24/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value))]
    concurrent_time_zone: list = [0 for _ in range(round(24/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value))]
    frequently_talked_topic: list = []
    frequently_used_emotion: list = [('', 0) for _ in range(6)]
    frequency_of_affection: float = 0
    number_of_love_words:int = 0
    sweetness_score:float = 0
    average_reply_term:timedelta = timedelta(0)

    def parse_to_json(self):
        return {
            'report_type' : self.report_type,
            'image' : self.image,
            'MBTI' : self.MBTI,
            'response_time_zone' : self.response_time_zone,
            'concurrent_time_zone' : self.concurrent_time_zone,
            'frequently_talked_topic' : self.frequently_talked_topic,
            'frequently_used_emotion' : self.frequently_used_emotion,
            'frequency_of_affection' : self.frequency_of_affection,
            'number_of_love_words' : self.number_of_love_words,
            'sweetness_score' : self.sweetness_score,
            'average_reply_term' : self.average_reply_term,
        }

'''
- 리포트로 분석해줄 항목
    - 연애 MBTI
    - 응답 시간대, 동시 접속 시간대 → 막대 그래프
    - 자주하는 이야기 주제 → 워드 클라우드 형식으로
    - 자주 사용하는 감정 표현, 각 감정표현 당 사용 빈도 → 육각 그래프
    - 애정표현 빈도, 사랑한다는 말의 횟수
    - 달달함 점수, 애정도 분석
    - 평균 답장 텀 / 연락 횟수 ( 둘이 합쳐서 )
- 작은 리포트
- 과거 리포트 기록
    - 썸네일 리스트가 뜨고, 눌렀을 때 상세 페이지로 이동
    - 일단은 전부 무료로 제공
- 리포트 분석 시나리오
    1. 리포트 페이지로 들어간다.
    2. 생성하기
    3. 기간 정하기
    4. 확인
- 리포트를 어떻게 생성해 줄거냐
    - 유저가 처음과 끝 설정 → 원하는 단위로 볼 수 있음
    - 원하는 단위로 볼 수 있는데 기간 `X token`안되면 대체품으로 만들어 주고 넘으면 원래 리포트
        - 사진생성 한개 → 다른 분류체계 만들어가지고 이때는 바빴어요.
- 정책
    - 얼마나 생성할 수 있는가 (일주일에 한 개)
    - 카톡 불러오기 없음
- 리포트 생성
    - 달력에서 선택
    - 시작 날짜와 끝 날짜의  D-Day도 같이보여줌 (이걸로도 설정 가능)
'''