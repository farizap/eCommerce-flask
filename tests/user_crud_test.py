import json
from . import app, client, cache, create_token_admin, create_token_shop, create_token, create_token_user_test


class TestShopCrud():

########## post

    def test_post_user_invalid(self, client):

        data = {
            "address": "asdasd",
            'name': 'TEST'
        }
        res = client.post('/users/register', data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_user_valid(self, client):



        data = {
            "client_secret": "TEST",
            "client_key": "TEST",
            "address": "test address",
            "contact": "test@test.com",
            'name': 'TEST',
            "age": 12,
            'sex': 'male',
        }

        res = client.post('/users/register', data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestShopCrud.shop_id  = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200


############ get by id
    def test_get_by_id_user_valid(self, client):
        token = create_token_user_test()
        res = client.get(f'/users/me' , headers={'Authorization':'Bearer ' + token})
    
        assert res.status_code == 200


    def test_get_by_id_user_invalid(self, client):
        token = create_token_user_test()
       

        res = client.get('/users/0' , headers={'Authorization':'Bearer ' + token})
        
    
        assert res.status_code == 404


############### put by id
    def test_put_user_valid(self, client):
        token = create_token()
       
        data = {
            'name': 'TEST',
        }

        res = client.put(f'/users/me', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_user_invalid(self, client):
        token = create_token_user_test()
       
        data = {
        'clissent_key': 'CLIENT05',
        'stsock': '0',
        }

        res = client.put(f'/users/0', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 404

# delete by id
    def test_delete_user_invalid(self, client):
        token = create_token_user_test()

        res = client.delete('/users/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 404
    def test_delete_user_valid(self, client):
        token = create_token_user_test()

        res = client.delete(f'/users/me', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 200
    

