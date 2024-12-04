from flask import Flask
from app.utils.helpers import db,bcrypt,register_filters,register_blueprints
from app.config import Config,TestingConfig
import os
from sqlalchemy import text


def create_app():

    app = Flask(__name__)

    if os.environ.get('FLASK_ENV') == 'testing':

        app.config.from_object(TestingConfig)
        app.app_context().push()
    else: 
         app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        try: 
              db.session.execute(text('SELECT 1'))
              print(f"\n\n Connection to database is successful 😬 \n\n")
        except Exception as e: 
            print(f"Database connection failed {e}")

    register_filters(app)
    register_blueprints(app)

    return app


