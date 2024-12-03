

import os 
import pytest 
from sqlalchemy import inspect,text
from ..data import db 




def test_connection(client):

    
    app = client.application
    with app.app_context():
        
        res = db.session.execute(text("Select 1"))

        assert res.scalar() == 1

    
    assert False == False
