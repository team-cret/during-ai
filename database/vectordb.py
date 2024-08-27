
class VectorDB:
    def __init__(self) -> None:
        pass

    def insertData(self, groupId, vectorData):
        pass

    def removeDataByChatId(self, groupId, chatId):
        pass

    def retrieve_data(self, groupId, userData):
        return ['', '', '', '', '']
    
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from model.data_model import CoupleChat, GomduChat, RetrievedData
from setting.config import Config
from setting.db_config import DBConfig

class VectorDB:
    def __init__(self) -> None:
        DATABASE_URL = DBConfig.DATABASE_URL.value
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()

    def retrieve_data(self, couple_id:int, embedded_data:list[float]) -> list[RetrievedData]:
        try:
            query_vector_str = embedded_data.tolist()
            query_vector_sql = str(query_vector_str).replace('[', '{').replace(']', '}')

            sql = text(f"""
                WITH query AS (
                    SELECT '{query_vector_sql}'::VECTOR(300) AS q
                )
                SELECT id, name, embedding,
                    1 - (embedding <=> q) AS similarity
                FROM items, query
                ORDER BY similarity DESC
                LIMIT :limit;
            """)
            session = self.get_session()
            query = session.query(RetrievedData).filter(
                RetrievedData.couple_id == couple_id,
            ).order_by(RetrievedData.chat_id)

            retrieved_data = query.all()
            
            session.close()
            return retrieved_data
        except Exception as e:
            print(f"데이터베이스에서 채팅 데이터를 가져오는 중 오류 발생: {str(e)}")
            return []


