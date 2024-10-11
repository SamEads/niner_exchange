import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_CON_STR')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Secure'