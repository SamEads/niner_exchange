from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1999@localhost:5432/postgres'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def test_connection():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print("Database connection is OK:", result.fetchone())
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    with app.app_context():  
        test_connection()
