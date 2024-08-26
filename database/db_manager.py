import psycopg2
from psycopg2 import OperationalError

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# SQLAlchemy의 기본 클래스
Base = declarative_base()

class CoupleChat(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

class DBManager:
    def __init__(self, dbname, user, password, host, port=5432):
        """
        Initialize the PostgreSQLConnectionManager with connection parameters.

        :param dbname: Database name
        :param user: Username
        :param password: Password
        :param host: Hostname or IP address
        :param port: Port number (default is 5432)
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """
        Establish a connection to the PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connection to PostgreSQL established.")
        except OperationalError as e:
            print(f"Error: {e}")
            self.connection = None
            self.cursor = None
    
    def execute_query(self, query, params=None):
        """
        Execute a SQL query.

        :param query: SQL query string
        :param params: Optional query parameters
        :return: Result of the query
        """
        if not self.cursor:
            raise ConnectionError("Not connected to the database.")
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Query failed: {e}")
            self.connection.rollback()
            return None
    
    def close(self):
        """
        Close the connection to the PostgreSQL database.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection to PostgreSQL closed.")

    def __enter__(self):
        """
        Enable usage of the class in a 'with' statement.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensure the connection is closed when exiting the 'with' statement.
        """
        self.close()
