import pytest 
import os 

from app import create_app
from data import db 
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
    clear_procedure = """
    DO $$ 
    DECLARE 
        table_name text; 
    BEGIN 
        -- Loop through each table in the Test_Niner_Ex schema
        FOR table_name IN (SELECT tablename FROM pg_tables WHERE schemaname = 'Test_Niner_Ex') 
        LOOP 
            -- Execute TRUNCATE on each table, CASCADE ensures dependent records are also removed
            EXECUTE 'TRUNCATE TABLE ' || quote_ident('Test_Niner_Ex.' || table_name) || ' CASCADE'; 
        END LOOP; 
    END $$;
    """
    
    db.session.execute(text(clear_procedure))
    db.session.commit()  # Commit the changes to the database
