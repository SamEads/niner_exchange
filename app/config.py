import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_CON_STR')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Secure'
    SCHEMA = "Niner_Exchange"



class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_CON_STR')
    SCHEMA = "Test_Niner_Ex"
