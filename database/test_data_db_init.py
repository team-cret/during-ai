from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import psycopg2
import numpy as np
from tqdm import tqdm

# 데이터베이스 연결 문자열
DATABASE_URL = "postgresql+psycopg2://postgres:sync314159@127.0.0.1:5432/during_test"

# 엔진 생성
engine = create_engine(DATABASE_URL)
print('success create engine')

# 메타데이터 객체 생성
metadata = MetaData()
print('success create metadata')

# 연결 생성
Session = sessionmaker(bind=engine)
session = Session()
print('success create session')
# 테이블 객체 생성
chunk_table = Table('chunk', metadata, autoload_with=engine, schema='during_test')
couple_chat_message_table = Table('couple_chat_message', metadata, autoload_with=engine, schema='during_test')
chunked_couple_chat_table = Table('chunked_couple_chat', metadata, autoload_with=engine, schema='during_test')
print('success create table')

# insert query 실행
couple_id = 314159265
chat_id = 0
try:
    new_chat_messages = []
    new_chunks = []
    new_chunked_couple_chats = []
    with open('./database/KakaoTalkChats.txt', 'r', encoding='utf-8') as chat_file:
        with open('./database/kakaoChatEmbedding.txt', 'r', encoding='utf-8') as embedding_file:
            chat_lines = chat_file.readlines()
            embedding_lines = list(embedding_file.readlines())
            chunks = [chat_lines[i:(i+100) if i + 100 < len(chat_lines) else len(chat_lines)] for i in range(0, len(chat_lines), 100)]
            for i, (chunk, vector) in tqdm(enumerate(zip(chunks, embedding_lines))):
                couple_chat_ids = []
                summary = ''
                for chat in chunk:
                    try:
                        if len(chat) < 10:
                            continue
                        a = str(chat)
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
                        message_start = a[f+2:].find(':')
                        member_id_str = a[f+2:f+2+message_start-1]
                        member_id = 1 if member_id_str == '박건우' else 2
                        chat_id += 1
                        new_chat_message = {
                            'couple_chat_id' : chat_id,
                            'chat_type' : 'text',
                            'context' : a[f+2+message_start+1:],
                            'chat_date' : date.strftime('%Y-%m-%d %H:%M:%S'),
                            'send_member_id' : member_id,
                            'couple_id' : couple_id,
                        }
                        
                        summary += new_chat_message['context']
                        couple_chat_ids.append(new_chat_message['couple_chat_id'])
                        new_chat_messages.append(new_chat_message)
                        chat_id += 1
                    except Exception:
                        continue
                vector = list(map(float, vector.split()))
                vector = np.array(vector, dtype=np.float64).tolist()
                new_chunk = {
                    'chunk_id' : i,
                    'vector' : vector,
                    'summary' : summary,
                    'couple_id' : couple_id
                }
                new_chunks.append(new_chunk)
                for chat_id in couple_chat_ids:
                    new_chunked_couple_chats.append({
                        'chunk_id' : i,
                        'couple_chat_id' : chat_id
                    })
    try:
        session.execute(couple_chat_message_table.insert(), new_chat_messages)
        session.execute(chunk_table.insert(), new_chunks)
        session.execute(chunked_couple_chat_table.insert(), new_chunked_couple_chats)
        session.commit()
    except Exception as e:
        print(e)
except Exception as e:
    print(e)

print('success execute query')
# 세션 종료
session.close()
print('success close session')
