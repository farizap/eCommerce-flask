import json
from . import app, client, cache, create_token_admin, create_token_shop, create_token


class TestShopCrud():

    shop_id = 0


# ########### get list
#     def test_get_Shop_list_valid(self, client):
#         res = client.get('/shop/all')

#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_get_Shop_list_invalid(self, client):
#         res = client.get('/shop/lsst')


#         res_json = json.loads(res.data)
#         assert res.status_code == 404

########## post

    def test_post_Shop_invalid(self, client):
        token = create_token()

        data = {
            "address": "asdasd",
            'name': 'TEST'
        }
        res = client.post('/shop/register', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_Shop_valid(self, client):
        
        token = create_token()

        data = {
            "address": "asdasd",
            'name': 'TEST',
            'city': 'test',
            'contact': 400000,
        }

        res = client.post('/shop/register', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestShopCrud.shop_id  = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200


############ get by id
    def test_get_by_id_Shop_valid(self, client):

        res = client.get(f'/shop/{TestShopCrud.shop_id }')
    
        assert res.status_code == 200


    def test_get_by_id_Shop_invalid(self, client):
       

        res = client.get('/shop/0')
        
    
        assert res.status_code == 404


############### put by id
    def test_put_shop_valid(self, client):
        token = create_token()
       
        data = {
            "address": "asdasd",
            'name': 'TEST',
            'city': 'test',
            'contact': 400000,
        }

        res = client.put(f'/shop/{TestShopCrud.shop_id }', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_shop_invalid(self, client):
        token = create_token()
       
        data = {
        'clissent_key': 'CLIENT05',
        'stsock': '0',
        }

        res = client.put(f'/shop/0', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 500

# delete by id
    def test_delete_shop_valid(self, client):
        token = create_token()

        res = client.delete(f'/shop/{TestShopCrud.shop_id }', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 200
    
    def test_delete_shop_invalid(self, client):
        token = create_token()

        res = client.delete('/shop/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 403

