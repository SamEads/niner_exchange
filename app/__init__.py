from flask import Flask
from flask_bcrypt import Bcrypt
from utils.helpers import db,bcrypt
from config import Config,TestingConfig
from routes import register_blueprints
from utils.helpers import register_filters
import os
from sqlalchemy import text

def create_app():
    app = Flask(__name__)
    app.config.from_object(TestingConfig if app.config['TESTING'] else Config)
    
    print(f"\n\n{os.getenv('DB_CON_STR')}\n\n") 

    if os.environ.get('FLASK_ENV') == 'testing':
            app.config.from_object(TestingConfig)
            app.app_context().push()
    else: 
         app.config.from_object(Config)
        
    bcrypt.init_app(app)


    with app.app_context():
        try: 
              db.session.execute(text('SELECT 1'))
              print(f"\n\nConnected to {db.engine.url.render_as_string(hide_password=False)}\n\n")
        except Exception as e: 
    
            print(f"Database connection failed {e}")

    db.init_app(app)
    register_filters(app)

    register_blueprints(app)

    return app



def register_blueprints(app):

    from .routes import (
    auth_bp,
    user_bp,
    listing_bp,
    messaging_bp,
    inbox_bp,
    setting_bp,
    info_bp
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(messaging_bp)
    app.register_blueprint(inbox_bp)
    app.register_blueprint(setting_bp)
    app.register_blueprint(info_bp)
