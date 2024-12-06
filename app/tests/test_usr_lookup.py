from ..data.models import Users,Friendship
import random 
import string



def test_lookup(client):

    N = random.randrange(start=5,stop=50)
    pick = random.randrange(1,N//2)
    search_usr = None
    
    for i in range(N):

        n = random.randrange(start=2,stop=9)
        gen_usr = {
            'username' : ''.join(random.choices(string.ascii_letters + string.digits, k=n)),
            'password' :  ''.join(random.choices(string.ascii_letters + string.digits, k=n)),
            'class_level' : random.randrange(1,4)
        }
        if i == pick: 
            search_usr = gen_usr['username']

        response = client.post("/create",data=gen_usr)
        assert response.status_code == 302
    

    response = client.get(f'/user_search/1?query={search_usr}', follow_redirects=True)
    print(response.data.decode('utf-8'))
    print(response.request.path)
    assert f'<h5 class="card-title">{search_usr}</h5>' in response.data.decode('utf-8')





    

        

    


   
    

