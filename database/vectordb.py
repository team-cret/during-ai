from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database.db_security_manager import DBSecurityManager
from model.data_model import CoupleChat, GomduChat, RetrievedData
from model.db_model import Chunk, ChunkedCoupleChat
from setting.service_config import ServiceConfig
from setting.env_setting import EnvSetting

db_schema_type = {
    'test' : ServiceConfig.DB_TEST_SCHEMA_NAME.value,
    'dev' : ServiceConfig.DB_DEV_SCHEMA_NAME.value,
    'live' : ServiceConfig.DB_LIVE_SCHEMA_NAME.value,
}

class VectorDB:
    def __init__(self) -> None:
        self.set_db()
        self.db_encryptor = DBSecurityManager()
    
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
                FROM {db_schema_type[ServiceConfig.DB_CURRENT_TYPE.value]}.{ServiceConfig.DB_RETRIEVAL_TABLE_NAME.value}
                WHERE couple_id = :couple_id
                ORDER BY distance 
                LIMIT :limit
                """
            )
            retrieved_data = session.execute(
                sql, 
                {
                    "limit": ServiceConfig.DB_RETRIEVAL_TOP_K.value, 
                    "vec": query_vector_sql,
                    "couple_id": couple_id
                }
            ).fetchall()
            
            parsed_data = []
            for data in retrieved_data:
                parsed_data.append(RetrievedData(
                    chunk_id=data.chunk_id,
                    similarity=data.distance,
                    summary=self.db_encryptor.decode_message(data.summary),
                ))

            session.close()
            return parsed_data
        except Exception as e:
            session.rollback() 
            print(f"데이터베이스에서 데이터를 가져오는 중 오류 발생: {str(e)}")
            return []
        finally:
            if session:
                session.close()

    def insert_chunks(self, embedded_couple_chat:list[Chunk]) -> bool:
        try:
            session = sessionmaker(bind=self.engine, expire_on_commit=False)()
            session.add_all(embedded_couple_chat)
            session.commit()
            session.close()

            return True
        except Exception as e:
            session.rollback() 
            print(f"데이터베이스에서 데이터를 가져오는 중 오류 발생: {str(e)}")
            return False
        finally:
            if session:
                session.close()
        
    def insert_chunked_couple_chat(self, chunked_couple_chat:list[ChunkedCoupleChat]):
        try:
            session = sessionmaker(bind=self.engine, expire_on_commit=False)()
            session.add_all(chunked_couple_chat)
            session.commit()
            session.close()

            return True
        except Exception as e:
            session.rollback() 
            print(f"데이터베이스에서 데이터를 가져오는 중 오류 발생: {str(e)}")
            return False
        finally:
            if session:
                session.close()

    def delete_all_chunks(self) -> bool:
        try:
            session = self.get_session()
            session.query(Chunk).delete()
            session.commit()
            session.close()

            return True
        except Exception as e:
            session.rollback() 
            print(f"데이터베이스에서 데이터를 가져오는 중 오류 발생: {str(e)}")
            return False
        finally:
            if session:
                session.close()
    
    def delete_all_chunked_couple_chat(self) -> bool:
        try:
            session = self.get_session()
            session.query(ChunkedCoupleChat).delete()
            session.commit()
            session.close()

            return True
        except Exception as e:
            session.rollback() 
            print(f"데이터베이스에서 데이터를 가져오는 중 오류 발생: {str(e)}")
            return False
        finally:
            if session:
                session.close()