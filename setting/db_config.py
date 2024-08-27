from enum import Enum

class DBConfig(Enum):
    # Key Configuration
    #------------------------------------------------#
    DATABASE_URL = "postgresql+psycopg2://postgres:sync314159@127.0.0.1:5432/during_test"
    DATABASE = "postgresql+psycopg2"
    DATABASE_NAME = "during_test"
    DATABASE_USER = "postgres"
    DATABASE_PASSWORD = "sync314159"
    DATABASE_HOST = "127.0.0.1"
    DATABASE_PORT = "5432"
    #------------------------------------------------#