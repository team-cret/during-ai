
# class VectorDB:
#     def __init__(self) -> None:
#         pass

#     def insertData(self, groupId, vectorData):
#         pass

#     def removeDataByChatId(self, groupId, chatId):
#         pass

#     def retrieve_data(self, groupId, userData):
#         return ['', '', '', '', '']
    
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from model.data_model import CoupleChat, GomduChat, RetrievedData
from setting.service_config import ServiceConfig
from setting.env_setting import EnvSetting

class VectorDB:
    def __init__(self) -> None:
        self.set_db()
    
    def set_db(self):
        DATABASE_URL = EnvSetting().db_url
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()

    def retrieve_data(self, couple_id:str, embedded_data:list[float]) -> list[RetrievedData]:
        try:
            session = self.get_session()
            query_vector_str = embedded_data.tolist()
            query_vector_sql = str(query_vector_str).replace('[', '{').replace(']', '}')

            sql = text(f"""
                WITH query AS (
                    SELECT '{query_vector_sql}'::VECTOR({ServiceConfig.GOMDU_CHAT_EMBEDDING_DIMENSION.value}) AS q
                )
                SELECT id, name, embedding,
                    1 - (embedding <=> q) AS similarity
                FROM , query
                ORDER BY similarity DESC
                LIMIT :limit;
            """)
            
            query = session.query(RetrievedData).filter(
                RetrievedData.couple_id == couple_id,
            ).order_by(RetrievedData.chat_id)

            retrieved_data = query.all()
            
            session.close()
            return retrieved_data
        except Exception as e:
            print(f"데이터베이스에서 채팅 데이터를 가져오는 중 오류 발생: {str(e)}")
            return []


