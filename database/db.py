from model.data_model import CoupleChat
from setting.config import Config
from datetime import datetime

class DB:
    def __init__(self) -> None:
        pass

    def load_chat_data_for_period(self, couple_id:str, start_date:datetime, end_date:datetime) -> list[CoupleChat]:
        loaded_data = []
        with open('data/KakaoTalkChats.txt', 'r', encoding=Config.ENCODING_TYPE.value) as file:
            while True:
                try:
                    line = file.readline()
                    if len(line) < 10:
                        continue
                    
                    a = str(line)
                    b = a.find('년')
                    c = a.find('월')
                    d = a.find('일')
                    e = a.find(':')
                    f = a.find(',')
                    g = a[d+2:d+4]

                    date = datetime(
                        int(a[b-4:b]), 
                        int(a[b+2:c]), 
                        int(a[c+2:d]), 
                        int(a[d+5:e])%12 + (12 if g == '오후' else 0), 
                        int(a[e+1:f])
                    )

                    if date < start_date:
                        continue
                    if not line or date > end_date:
                        break
                    message_start = a[f+2:].find(':')
                    loaded_data.append({
                        'user_id' : a[f+2:f+2+message_start-1],
                        'couple_id' : couple_id,
                        'timestamp' : date,
                        'message' : a[f+2+message_start+1:],
                    })
                except Exception:
                    # print(line)
                    # print(Exception)
                    continue
        
        print('loaded data : ', len(loaded_data))
        parsed_data = []
        for data in loaded_data:
            parsed_data.append(self.parse_couple_chat(data))

        print('parsed data : ', len(parsed_data))
        return parsed_data
    
    def parse_couple_chat(self, chat_db_row:dict) -> CoupleChat:
        return CoupleChat(
            user_id=chat_db_row['user_id'],
            couple_id=chat_db_row['couple_id'],
            timestamp=chat_db_row['timestamp'],
            message=chat_db_row['message']
        )

    def get_gomdu_history(self, groupId, memberId, size):
        return []