from flask import Flask
from flask_bcrypt import Bcrypt
from data.models import db
from config import Config
from routes import register_blueprints

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)

db.init_app(app)

with app.app_context():
    register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)