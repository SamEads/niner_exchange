from flask_sqlalchemy import SQLAlchemy
from datetime import date
db = SQLAlchemy()



class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    class_level = db.Column(db.Integer, nullable=False)  # Class level (1-4)
    created_at = db.Column(db.DateTime, default=date.today())  # Account creation timestamp
    updated_at = db.Column(db.DateTime, default=date.today(), onupdate=date.today())  # Last update timestamp

    def __init__(self, username, password_hash, first_name, email, class_level):
        self.username = username
        self.password_hash = password_hash
        self.first_name = first_name
        self.email = email
        self.class_level = class_level  # Class level (1-4)


class Ratings(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)  # User being rated
    rater_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)  # User giving the rating
    rating = db.Column(db.Integer, nullable=False)  # Rating value (1-5)
    created_at = db.Column(db.DateTime, default=date.today())  # Timestamp for rating creation

    def __init__(self, user_id, rater_id, rating):
        self.user_id = user_id