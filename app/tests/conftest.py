import pytest 
import os 

from app import create_app
from ..utils.helpers import db 
from sqlalchemy import text 

@pytest.fixture()
def app():
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()

    clear_database()
    yield app
    clear_database() 



@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli.runner()

def clear_database():
    # SQL to truncate all tables in the Test_Niner_Ex schema

    try:
            with open("wipe_data.sql","r") as clear_procedure:
                db.session.execute(text(clear_procedure.read()))
                db.session.commit()  # Commit the changes to the database
    except Exception as e: 
        db.session.rollback()
        raise e
