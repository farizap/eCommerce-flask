import json
from . import app, client, cache, create_token_admin, create_token_shop, create_token


class TestProductCrud():

    product_id = 0


########### get list
    def test_get_Product_list_valid(self, client):
        res = client.get('/product/all')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_Product_list_invalid(self, client):
        res = client.get('/product/lsst')


        res_json = json.loads(res.data)
        assert res.status_code == 404

########## post

    def test_post_Product_invalid(self, client):
        token = create_token()
        data = {
            "category_id": 4,
            'name': 'TEST',
            'stock': 0,
            'price': 400000,
            'img_url': 'test_img_url',
            'description': 'testt' 
        }
        res = client.post('/product', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 403

    def test_post_Product_valid(self, client):
        token = create_token_shop()
       
        data = {
            "category_id": 4,
            'name': 'TEST',
            'img_url': 'test_img_url',
            'stock': 5,
            'price': 400000,
            'description': 'testt'
        }

        res = client.post('/product', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestProductCrud.product_id  = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200


############ get by id
    def test_get_by_id_Product_valid(self, client):

        res = client.get(f'/product/{TestProductCrud.product_id }')
    
        assert res.status_code == 200


    def test_get_by_id_Product_invalid(self, client):
       

        res = client.get('/product/0')
        
    
        assert res.status_code == 404


############### put by id
    def test_put_category_valid(self, client):
        token = create_token_shop()
       
        data = {
            "category_id": 4,
            'name': 'TEST_put',
            'img_url': 'test_img_url',
            'stock': 5,
            'price': 400000,
            'description': 'testt'
        }

        res = client.put(f'/product/{TestProductCrud.product_id }', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_category_invalid(self, client):
        token = create_token()
       
        data = {
        'client_key': 'CLIENT05',
        'stock': '0',
        }

        res = client.put(f'/product/{TestProductCrud.product_id }', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 403

# delete by id
    def test_delete_category_valid(self, client):
        token = create_token_shop()

        res = client.delete(f'/product/{TestProductCrud.product_id }', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 200
    
    def test_delete_category_invalid(self, client):
        token = create_token_shop()

        res = client.delete('/product/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 404

########### get list shop product
    def test_get_Shop_Product_list_valid(self, client):
        token = create_token_shop()
        res = client.get('/product/shop', headers={'Authorization':'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_Shop_Product_list_invalid(self, client):
        token = create_token_shop()
        res = client.get('/product/lsst', headers={'Authorization':'Bearer ' + token})


        res_json = json.loads(res.data)
        assert res.status_code == 404
