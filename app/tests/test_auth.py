

import os 
from sqlalchemy import inspect,text
from ..utils.helpers import bcrypt
from ..data.models import Users


#Tests if a user can sign up and then delete their account
def test_new_user(client):

    data = {
        'username' : "fake_user",
        'password' : "anything",
        'class_level' : 2
    }

    response = client.post("/create",data=data) 


    test_user = Users.query.filter_by(username=data['username']).first()

    assert test_user.username == data['username']
    assert test_user.class_level == data['class_level']
    assert bcrypt.check_password_hash(test_user.password_hash, data['password'])
    assert response.status_code == 302

    


    
    

