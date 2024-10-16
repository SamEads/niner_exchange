from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
db = SQLAlchemy()
import random,string

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

    
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.first_name = "Placeholder Name"
        self.email = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)) + '@' +''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))

        self.class_level = 1

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255), nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    edited = db.Column(db.Boolean, default=False)

class Ratings(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)  # User being rated
    rater_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)  # User giving the rating
    rating = db.Column(db.Integer, nullable=False)  # Rating value (1-5)
    created_at = db.Column(db.DateTime, default=date.today())  # Timestamp for rating creation

    def __init__(self, user_id, rater_id, rating):
        self.user_id = user_id


    #Get rating based on user ID
    def get_rating(user_id: int) -> int:

        ratings = Ratings.query.filter_by(user_id = user_id).all()

        if not ratings: 
            return -1

        actual = int(sum(rating.rating for rating in ratings) / len(ratings))

        return actual

class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable =False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship('Users', backref='listings')
