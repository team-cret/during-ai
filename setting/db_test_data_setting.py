from datetime import datetime

import numpy as np
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from init_setting import init_setting
init_setting()

from database.db import DB
from database.vectordb import VectorDB
from database.db_security_manager import DBSecurityManager
from model.data_model import ReportRequest
from model.db_model import CoupleChatMessage
from service.gomdu.chunker_v0 import ChunkerV0
from env_setting import EnvSetting
from service_config import ServiceConfig
DATABASE_URL = EnvSetting().db_url
engine = create_engine(DATABASE_URL)
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

# chunk_table = Table('chunk', metadata, autoload_with=engine, schema=ServiceConfig.DB_TEST_SCHEMA_NAME.value)
couple_chat_message_table = Table('couple_chat_message', metadata, autoload_with=engine, schema=ServiceConfig.DB_TEST_SCHEMA_NAME.value)
# chunked_couple_chat_table = Table('chunked_couple_chat', metadata, autoload_with=engine, schema=ServiceConfig.DB_TEST_SCHEMA_NAME.value)

couple_id = ServiceConfig.DB_TEST_COUPLE_ID.value
chat_id = 0

user1_id = ServiceConfig.DB_TEST_USER_ID_1.value
user2_id = ServiceConfig.DB_TEST_USER_ID_2.value
db = DB()
vectordb = VectorDB()
dbs = DBSecurityManager()

# migration another schema
# try:
#     MIN_DATE = datetime(1970, 1, 1)
#     MAX_DATE = datetime(9999, 12, 31)
#     couple_chat_message = db.b_get_couple_chat_for_period(
#         ReportRequest(
#             couple_id=couple_id,
#             start_date=MIN_DATE,
#             end_date=MAX_DATE
#         )
#     )
#     print(len(couple_chat_message))
#     if couple_chat_message:

#         couple_chat_message = [
#             {
#                 'couple_chat_message_id':chat.chat_id,
#                 'message_type':chat.chat_type,
#                 'content':dbs.encode_message(chat.message),
#                 'message_date':chat.timestamp,
#                 'send_member_id':chat.user_id,
#                 'couple_id':chat.couple_id
#             } for chat in couple_chat_message
#         ]

#         session.execute(couple_chat_message_table.insert(), couple_chat_message)
#         session.commit()
#         print('inserted new chat messages')
# except Exception as e:
#     print(e)
# finally:
#     if session:
#         session.close()

# chunking vectordbp
try:
    chunker = ChunkerV0()
    chunker.automatic_chunking()
    print('chunking success')
except Exception as e:
    print(e)

# chunked couple chat, chunk delete
# try:
#     vectordb.delete_all_chunked_couple_chat()
#     vectordb.delete_all_chunks()
#     print('deleted chunked couple chat and chunk')
# except Exception as e:
#     print(e)

# try:
#     new_chat_messages = []
#     new_chunks = []
#     new_chunked_couple_chats = []
#     with open('./database/KakaoTalkChats.txt', 'r', encoding='utf-8') as chat_file:
#         with open('./database/kakaoChatEmbedding.txt', 'r', encoding='utf-8') as embedding_file:
#             chat_lines = chat_file.readlines()
#             embedding_lines = list(embedding_file.readlines())
#             chunks = [chat_lines[i:(i+100) if i + 100 < len(chat_lines) else len(chat_lines)] for i in range(0, len(chat_lines), 100)]
#             for i, (chunk, vector) in tqdm(enumerate(zip(chunks, embedding_lines))):
#                 couple_chat_ids = []
#                 summary = ''
#                 for chat in chunk:
#                     try:
#                         if len(chat) < 10:
#                             continue
#                         a = str(chat)
#                         b = a.find('년')
#                         c = a.find('월')
#                         d = a.find('일')
#                         e = a.find(':')
#                         f = a.find(',')
#                         g = a[d+2:d+4]
#                         date = datetime(
#                             int(a[b-4:b]), 
#                             int(a[b+2:c]), 
#                             int(a[c+2:d]), 
#                             int(a[d+5:e])%12 + (12 if g == '오후' else 0), 
#                             int(a[e+1:f])
#                         )
#                         message_start = a[f+2:].find(':')
#                         member_id_str = a[f+2:f+2+message_start-1]
#                         member_id = ServiceConfig.DB_TEST_USER_ID_1.value if member_id_str == '박건우' else ServiceConfig.DB_TEST_USER_ID_2.value
#                         chat_id += 1
#                         new_chat_message = {
#                             'couple_chat_id' : chat_id,
#                             'chat_type' : 'text',
#                             'context' : a[f+2+message_start+1:],
#                             'chat_date' : date.strftime('%Y-%m-%d %H:%M:%S'),
#                             'send_member_id' : member_id,
#                             'couple_id' : couple_id,
#                         }
                        
#                         summary += new_chat_message['context']
#                         couple_chat_ids.append(new_chat_message['couple_chat_id'])
#                         new_chat_messages.append(new_chat_message)
#                         chat_id += 1
#                     except Exception:
#                         continue
#                 vector = list(map(float, vector.split()))
#                 vector = np.array(vector, dtype=np.float64).tolist()
#                 new_chunk = {
#                     'chunk_id' : i,
#                     'vector' : vector,
#                     'summary' : summary,
#                     'couple_id' : couple_id
#                 }
#                 new_chunks.append(new_chunk)
#                 for chat_id in couple_chat_ids:
#                     new_chunked_couple_chats.append({
#                         'chunk_id' : i,
#                         'couple_chat_id' : chat_id
#                     })
#     try:
#         session.execute(couple_chat_message_table.insert(), new_chat_messages)
#         print('inserted new chat messages')
#         session.execute(chunk_table.insert(), new_chunks)
#         print('inserted new chunks')
#         session.execute(chunked_couple_chat_table.insert(), new_chunked_couple_chats)
#         print('inserted new chunked couple chats')
#         session.commit()
#         print('committed')
#     except Exception as e:
#         print(e)
# except Exception as e:
#     print('exception')
# session.close()
# print('success close session')


