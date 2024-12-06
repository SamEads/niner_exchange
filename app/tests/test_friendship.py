from ..data.models import Users,Friendship



def test_friendship(client,other_client):


    user1 = {
        'username' : "fake_user",
        'password' : "anything",
        'class_level' : 2
    }
    
    user2 = {
        'username' : "other_fake_user",
        'password' : "anything",
        'class_level' : 2
    }

    res1 = client.post("/create",data=user1)
    res2 = other_client.post('/create',data=user2) 

    i_1 = Users.get_id_by_username(user1['username'])
    i_2 = Users.get_id_by_username(user2['username'])

    Friendship.send_friend_request(i_1, i_2)
    Friendship.accept_friend_request(i_2,i_1)

    status = Friendship.check_relationship(i_1,i_2)

    assert status == "accepted"
    

