import pytest 
import os 

from app import create_app
from ..data import db 
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



def clear_database():

    clear_procedure = """
    select tablename from pg_tables where schemaname = 'Test_Niner_Ex';

            DO $$
            DECLARE
                table_name text;
            BEGIN
                FOR table_name IN (SELECT tablename FROM pg_catalog.pg_tables where schemaname= 'public')
                LOOP
                    EXECUTE 'DELETE FROM ' || quote_ident(table_name) || ' CASCADE';
                END LOOP;
            END $$;
                    """
    
    db.session.execute(text(clear_procedure))
    db.session.commit()
