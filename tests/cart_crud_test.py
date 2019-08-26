import json
from . import app, client, cache, create_token_admin, create_token


class TestCartCrud():

    cart_id = 0


########### get list
    def test_get_Cart_list_valid(self, client):
        token = create_token()
        res = client.get('/cart', headers={'Authorization':'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_Cart_list_invalid(self, client):
        token = create_token()
        res = client.get('/carts',  headers={'Authorization':'Bearer ' + token})


        res_json = json.loads(res.data)
        assert res.status_code == 404

########## post

    def test_post_Cart_invalid(self, client):
        token = create_token()
        data = {
            "test": 2 
        }
        res = client.post('/product/6/cart', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_Cart_valid(self, client):
        token = create_token()
       
        data = {
            "qty": 1
        }

        res = client.post('/product/9/cart', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestCartCrud.cart_id = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200



############### put by id
    def test_put_Cart_valid(self, client):
        token = create_token()
       
        data = {
        'qty' : 2
        }

        res = client.put(f'/cart/{TestCartCrud.cart_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_Cart_invalid(self, client):
        token = create_token()
       
        data = {
        'test': "test"
        }

        res = client.put(f'/cart/{TestCartCrud.cart_id}', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 400

# delete by id
    def test_delete_Cart_valid(self, client):
        token = create_token()

        res = client.delete(f'/cart/{TestCartCrud.cart_id}', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 200
    
    def test_delete_Cart_invalid(self, client):
        token = create_token()

        res = client.delete('/cart/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 404

