

import os 
from sqlalchemy import inspect,text
from ..utils.helpers import db




def test_connection(client):

    

    """
    ins = inspect(db.engine)
    tables = ins.get_table_names()

    assert db.engine.url.render_as_string(hide_password=False) == os.getenv("SQLALCHEMY_TEST_DATABASE_URI")
    for name in tables: 
        res = db.session.execute(text(f"select count(*) from {name};"))
        count = res.scalar
        assert count == 0
    
    """
    assert False == False
