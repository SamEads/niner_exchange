from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



#data model for the user 
class Users(db.Model):


    def __init__(self,username,password_hash):
        self.username = username
        self.password_hash = password_hash
        self.first_name = 'placeholder'

    
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(255), unique=True, nullable=False) 
    first_name = db.Column(db.String(50), nullable=False)  
    password_hash = db.Column(db.String(255), nullable=False)
