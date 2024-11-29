import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_CON_STR')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Secure'



class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_CON_STR')
