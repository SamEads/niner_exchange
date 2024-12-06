

import os 
from sqlalchemy import inspect,text
from ..utils.helpers import db
from ..data.models import Users
from dotenv import load_dotenv
import random
import string



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
    
    

def test_user_created(client):

    N = random.randrange(start=5,stop=25)
    pick = random.randrange(1,N//2)
    
    for i in range(N):

        n = random.randrange(start=2,stop=9)
        gen_usr = {
            'username' : ''.join(random.choices(string.ascii_letters + string.digits, k=n)),
            'password' :  ''.join(random.choices(string.ascii_letters + string.digits, k=n)),
            'class_level' : random.randrange(1,4)
        }
        

        response = client.post("/create",data=gen_usr,follow_redirects=True)

        user = Users.query.filter_by(username=gen_usr['username'])

        assert user is not None
        assert response.status_code == 200
