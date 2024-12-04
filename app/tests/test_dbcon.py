

import os 
from sqlalchemy import inspect,text
from ..utils.helpers import db
from dotenv import load_dotenv



def test_connection(client):
    load_dotenv()

    ins = inspect(db.engine)
    tables = ins.get_table_names()

    ##Test database connection 
    assert db.engine.url.render_as_string(hide_password=False) == os.getenv("TEST_DB_CON_STR")

    #check if all of the tables are empty
    for name in tables: 
        res = db.session.execute(text(f"select count(*) from {name};"))
        count = res.scalar()
        assert count == 0
    
    

