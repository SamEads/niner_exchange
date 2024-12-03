from flask import Flask
from app.utils.helpers import db,bcrypt,register_filters
from app.config import Config,TestingConfig
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
    db.init_app(app)


    
    with app.app_context():
        try: 
              db.session.execute(text('SELECT 1'))
              print(f"\n\nConnected to {db.engine.url.render_as_string(hide_password=False)}\n\n")
        except Exception as e: 
    
            print(f"Database connection failed {e}")

    register_filters(app)

    register_blueprints(app)

    return app



def register_blueprints(app):

    from .routes import (
    auth,
    user,
    listing,
    messaging,
    inbox,
    setting,
    info
    )

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(user.user_bp)
    app.register_blueprint(listing.listing_bp)
    app.register_blueprint(messaging.messaging_bp)
    app.register_blueprint(inbox.inbox_bp)
    app.register_blueprint(setting.setting_bp)
    app.register_blueprint(info.info_bp)
