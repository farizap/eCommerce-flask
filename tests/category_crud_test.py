import json
from . import app, client, cache, create_token_admin


class TestCategoryCrud():

    category_id = 0


########### get list
    def test_get_Category_list_valid(self, client):
        res = client.get('/category/list')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_Category_list_invalid(self, client):
        res = client.get('/category/lsst')


        res_json = json.loads(res.data)
        assert res.status_code == 404

########## post

    def test_post_Category_invalid(self, client):
        token = create_token_admin()
        data = {
            "nameeee": 4 
        }
        res = client.post('/category', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_Category_valid(self, client):
        token = create_token_admin()
       
        data = {
            "name": "test"
        }

        res = client.post('/category', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestCategoryCrud.category_id = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200


############ get by id
    def test_get_by_id_Category_valid(self, client):

        res = client.get(f'/category/{TestCategoryCrud.category_id}')
    
        assert res.status_code == 200


    def test_get_by_id_Category_invalid(self, client):
       

        res = client.get('/category/0')
        
    
        assert res.status_code == 404


############### put by id
    def test_put_category_valid(self, client):
        token = create_token_admin()
       
        data = {
        'name' : 'test',
        'dummy': 0
        }

        res = client.put(f'/category/{TestCategoryCrud.category_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_category_invalid(self, client):
        token = create_token_admin()
       
        data = {
        'client_key': 'CLIENT05',
        'client_secret': 'SECRET05',
        }

        res = client.put(f'/category/{TestCategoryCrud.category_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 400

# delete by id
    def test_delete_category_valid(self, client):
        token = create_token_admin()

        res = client.delete(f'/category/{TestCategoryCrud.category_id}', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 200
    
    def test_delete_category_invalid(self, client):
        token = create_token_admin()

        res = client.delete('/category/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 404

