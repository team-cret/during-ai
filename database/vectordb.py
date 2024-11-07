from datetime import datetime
import logging

from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker

from database.db_security_manager import DBSecurityManager
from model.data_model import RetrievedData
from model.db_model import Chunk, ChunkedCoupleChat, ChunkedRowNumber
from setting.service_config import ServiceConfig
from setting.env_setting import EnvSetting
from setting.logger_setting import logger_setting

db_schema_type = {
    'test' : ServiceConfig.DB_TEST_SCHEMA_NAME.value,
    'dev' : ServiceConfig.DB_DEV_SCHEMA_NAME.value,
    'live' : ServiceConfig.DB_LIVE_SCHEMA_NAME.value,
}

class VectorDB:
    def __init__(self) -> None:
        self.set_db()
        self.db_encryptor = DBSecurityManager()
        logger_setting()
        self.logger = logging.getLogger(__name__)   
    
    def set_db(self):
        DATABASE_URL = EnvSetting().db_url
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()
    
    #--------------------------------- create ----------------------------------#
    def insert_chunked_row_numbers(self, chunked_row_numbers:list[ChunkedRowNumber]) -> bool:
        try:
            session = self.get_session()
            session.add_all(chunked_row_numbers)
            session.commit()
            session.close()

            return True
        except Exception as e:
            session.rollback() 
            self.logger.error(f"Error in insert chunked row numbers: {str(e)}", exc_info=True)
            return False
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
            self.logger.error(f"Error in insert chunk: {str(e)}", exc_info=True)
            return False
        finally:
            if session:
                session.close()
    
    def insert_chunked_couple_chat(self, chunked_couple_chat:list[ChunkedCoupleChat]):
        try:
            session = self.get_session()
            session.add_all(chunked_couple_chat)
            session.commit()
            session.close()

            return True
        except Exception as e:
            session.rollback() 
            self.logger.error(f"Error in insert chunked couple chat: {str(e)}", exc_info=True)
            return False
        finally:
            if session:
                session.close()
    #---------------------------------------------------------------------------#    

    #---------------------------------- read -----------------------------------#
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
            self.logger.error(f"Error in retrieving data: {str(e)}", exc_info=True)
            return []
        finally:
            if session:
                session.close()

    def get_chunked_row_numbers(self) -> dict[str, tuple[int, int]]:
        try:
            session = self.get_session()
            query = session.query(ChunkedRowNumber)
            
            chunked_row_numbers = query.all()
            
            session.close()
            result = {}
            for chunked_row_number in chunked_row_numbers:
                result[chunked_row_number.couple_id] = (chunked_row_number.chunked_row_number_id, chunked_row_number.row_number)
            return result
        except Exception as e:
            self.logger.error(f"Error in getting chunked row number: {str(e)}", exc_info=True)
            return []
        finally:
            if session:
                session.close()
    
    def get_last_chunks_for_couple(self) -> list[RetrievedData]:
        try:
            session = self.get_session()
        
            subquery = (
                session.query(
                    Chunk.couple_id,
                    func.max(Chunk.chunk_id).label('max_chunk_id')
                )
                .group_by(Chunk.couple_id)
                .subquery()
            )

            results = (
                session.query(Chunk)
                .join(subquery, (Chunk.couple_id == subquery.c.couple_id) & (Chunk.chunk_id == subquery.c.max_chunk_id))
                .all()
            )
            session.close()

            return results
        except Exception as e:
            self.logger.error(f"Error in getting last chunks for couple: {str(e)}", exc_info=True)
            return []
        finally:
            if session:
                session.close()
    
    def get_max_chunk_id(self) -> int:
        try:
            session = self.get_session()
            query = session.query(func.max(Chunk.chunk_id)).scalar()
            session.close()

            if query == None:
                return 0
            return int(query)
        except Exception as e:
            self.logger.error(f"Error in getting max chunk id: {str(e)}", exc_info=True)
            raise Exception("Error in getting max chunk id")
        finally:
            if session:
                session.close()
    
    def get_max_chunked_couple_chat_id(self) -> int:
        try:
            session = self.get_session()
            query = session.query(func.max(ChunkedCoupleChat.chunked_couple_chat_id)).scalar()
            session.close()
            if query == None:
                return 0
            return int(query)
        except Exception as e:
            self.logger.error(f"Error in getting max chunked couple chat id: {str(e)}", exc_info=True)
            raise Exception("Error in getting max chunked couple chat id")
        finally:
            if session:
                session.close()

    #---------------------------------------------------------------------------#
    
    #--------------------------------- update ----------------------------------#
    def update_chunked_row_numbers(self, chunked_row_numbers:list[ChunkedRowNumber]) -> bool:
        try:
            session = self.get_session()

            for chunked_row_number in chunked_row_numbers:
                session.query(ChunkedRowNumber).filter(
                    ChunkedRowNumber.chunked_row_number_id == chunked_row_number.chunked_row_number_id
                ).update({ChunkedRowNumber.row_number: chunked_row_number.row_number})
            
            session.commit()
            session.close()
        except Exception as e:
            session.rollback() 
            self.logger.error(f"Error in updating chunked row numbers: {str(e)}", exc_info=True)
            return False
        finally:
            if session:
                session.close()
    #---------------------------------------------------------------------------#

    #--------------------------------- delete ----------------------------------#
    def delete_all_chunks(self) -> bool:
        try:
            session = self.get_session()
            session.query(Chunk).delete()
            session.commit()
            session.close()

            return True
        except Exception as e:
            session.rollback() 
            self.logger.error(f"Error in delete all chunk: {str(e)}", exc_info=True)
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
            self.logger.error(f"Error in delete all chunked couple chat: {str(e)}", exc_info=True)
            return False
        finally:
            if session:
                session.close()
    
    def delete_chunk_by_chunk_id(self, chunk_ids:list[int]) -> bool:
        try:
            session = self.get_session()
            session.query(Chunk).filter(Chunk.chunk_id.in_(chunk_ids)).delete(synchronize_session=False)
            session.commit()
            session.close()

            return True
        except Exception as e:
            session.rollback() 
            self.logger.error(f"Error in delete chunk by chunk id: {str(e)}", exc_info=True)
            return False
        finally:
            if session:
                session.close()

    def delete_chunked_couple_chat_by_chunk_id(self, chunk_ids:list[int]) -> bool:
        try:
            session = self.get_session()
            session.query(ChunkedCoupleChat).filter(ChunkedCoupleChat.chunk_id.in_(chunk_ids)).delete(synchronize_session=False)
            session.commit()
            session.close()

            return True
        except Exception as e:
            session.rollback() 
            self.logger.error(f"Error in delete chunked couple chat by chunk id: {str(e)}", exc_info=True)
            return False
        finally:
            if session:
                session.close()
    #---------------------------------------------------------------------------#    