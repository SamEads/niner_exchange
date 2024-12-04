import os
from dotenv import load_dotenv

load_dotenv()
class Config(object):
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_CON_STR')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Secure'
    SCHEMA = "Niner_Exchange"
    TESTING = False
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class TestingConfig(Config):
    
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_CON_STR')
    TESTING = True
    SCHEMA = "Test_Niner_Ex"
