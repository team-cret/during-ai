
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
from model.db_model import Chunk
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
            query_vector_sql = str(embedded_data)

            sql = text(
                f"""
                SELECT chunk_id, vector <-> :vec AS distance, summary
                FROM {ServiceConfig.DB_SCHEMA_NAME.value}.{ServiceConfig.DB_RETRIEVAL_TABLE_NAME.value}
                WHERE couple_id = :couple_id
                ORDER BY distance 
                LIMIT :limit
                """
            )
            retrieved_data = session.execute(
                sql, 
                {
                    "limit": ServiceConfig.RETRIEVAL_TOP_K.value, 
                    "vec": query_vector_sql,
                    "couple_id": couple_id
                }
            ).fetchall()
            
            parsed_data = []
            for data in retrieved_data:
                parsed_data.append(RetrievedData(
                    chunk_id=data.chunk_id,
                    similarity=data.distance,
                    summary=data.summary,
                ))

            session.close()
            return parsed_data
        except Exception as e:
            print(f"데이터베이스에서 채팅 데이터를 가져오는 중 오류 발생: {str(e)}")
            return []


