from flask_sqlalchemy import SQLAlchemy
from datetime import date
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




class Ratings(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)  # User being rated
    rater_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)  # User giving the rating
    rating = db.Column(db.Integer, nullable=False)  # Rating value (1-5)
    created_at = db.Column(db.DateTime, default=date.today())  # Timestamp for rating creation

    user = db.relationship('Users', foreign_keys=[user_id])
    rater = db.relationship('Users', foreign_keys=[rater_id])

    def __init__(self, user_id, rater_id, rating):
        self.user_id = user_id