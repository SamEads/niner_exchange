from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from app import app


db = SQLAlchemy()
bcrypt = Bcrypt()

# Grade level of student
def level(arg: int) -> str:
    match arg:
        case 1:
            return "1st"
        case 2:
            return "2nd"
        case 3:
            return "3rd"
        case 4:
            return "4th"

def format_timestamp(value):
    now = datetime.now(timezone.utc)
    if value.date() == now.date():
        return f"Today at {value.strftime('%I:%M %p')}"
    elif value.date() == (now - timedelta(days=1)).date():
        return f"Yesterday at {value.strftime('%I:%M %p')}"
    else:
        return value.strftime('%m/%d/%y at %I:%M %p')

def register_filters(app):
    app.jinja_env.filters['format_timestamp'] = format_timestamp


def register_blueprints(app):

    from ..routes import (
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