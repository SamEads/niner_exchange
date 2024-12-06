from ..data.models import Users
import random 
import string



def test_crud_user(client):

    n = random.randrange(start=5,stop=100)

    gen_usr = {
            'username' : ''.join(random.choices(string.ascii_letters + string.digits, k=n)),
            'password' :  ''.join(random.choices(string.ascii_letters + string.digits, k=n)),
            'class_level' : random.randrange(1,4)
        }
    
    #CREATE
    response = client.post('/create',data=gen_usr,follow_redirects=True)

    
    #READ
    assert f"<h2>{gen_usr['username']}</h2>" in response.data.decode('utf-8')
    with client.session_transaction() as session: 
        session['username'] = gen_usr['username']
        response = client.get('/settings')
        curr_usr_obj = Users.query.filter_by(username=gen_usr['username']).first()
        assert f'<input type="text" class="form-control" id="email" name="email" value="{curr_usr_obj.email}">' in response.data.decode('utf-8')
        assert f'<input type="text" class="form-control" id="username" name="username" value="{curr_usr_obj.username}">' in response.data.decode('utf-8')
    
    #UPDATE 
        new_features = {
            'email' : ''.join(random.choices(string.ascii_letters + string.digits, k=n)),
            'password' :  ''.join(random.choices(string.ascii_letters + string.digits, k=n)),
            'class-level' : random.randrange(1,4)
        }
        client.post('/settings',data=new_features)
        response = client.get('/settings')
        curr_usr_obj = Users.query.filter_by(username=gen_usr['username']).first()
        assert f'<input type="text" class="form-control" id="email" name="email" value="{curr_usr_obj.email}">' in response.data.decode('utf-8')
        assert f'<input type="text" class="form-control" id="username" name="username" value="{curr_usr_obj.username}">' in response.data.decode('utf-8')
    
    #DELETE 
        response = client.post('/delete',follow_redirects=True)
        session.clear()
        print(response.data.decode('utf-8'))
        curr_usr_obj = Users.query.filter_by(username=gen_usr['username']).first()
        assert curr_usr_obj is None
        assert session.get('username') is None
        
        
    





    

        

    


   
    

