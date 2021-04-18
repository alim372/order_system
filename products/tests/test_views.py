from .test_setup import TestSetUp
import pdb

class TestViews(TestSetUp):
    """"""""""""""""""""""""""""""""""""""""""
    # products admin control testing 
    """"""""""""""""""""""""""""""""""""""""""

    def test_create_new_product_with_no_token(self):
        res = self.client.post(self.products_create_for_admin_url , follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 401)
    
    def test_create_new_product_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + 'invalid token')
        res = self.client.post(self.products_create_for_admin_url, self.valid_product_data, format="json", follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 401)
    
    def test_create_new_product_with_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        res = self.client.post(self.products_create_for_admin_url, self.valid_product_data, format="json", follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 403)
    
    def test_create_new_product_with_admin_token_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        res = self.client.post(self.products_create_for_admin_url, self.valid_product_data, format="json", follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['data']['name'], self.valid_product_data['name'])
        self.assertEqual(res.data['data']['price_eur'], self.valid_product_data['price_eur'])
        self.assertEqual(res.data['data']['description'], self.valid_product_data['description'])
    
    def test_create_new_product_with_invalid_price_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        res = self.client.post(self.products_create_for_admin_url, self.invalid_price_product_data, format="json", follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 422)
        
    
    def test_create_new_product_with_incomplete_data(self):
        temp = self.valid_product_data
        self.valid_product_data.pop('name') #remove name and then test 
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        res = self.client.post(self.products_create_for_admin_url, self.valid_product_data, format="json", follow=True)
        
        self.assertEqual(res.status_code, 422)
        self.valid_product_data = temp
        self.valid_product_data.pop('price_eur') #remove price_eur and then test 
        res = self.client.post(self.products_create_for_admin_url, self.valid_product_data, format="json", follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 422)

    def test_records_products_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        res = self.client.get(self.products_records_for_admin_url, format="json", follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['meta']['total'], len(self.test_bulk_products))
        self.assertEqual(len(res.data['data']), len(self.test_bulk_products))
        # pdb.set_trace()
    
    def test_records_products_data_with_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        res = self.client.get(self.products_records_for_admin_url, format="json", follow=True)
        self.assertEqual(res.status_code, 403)
        # pdb.set_trace()
    
    
    def test_exist_single_record_products(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        exist_product_id = '200'
        res = self.client.get(self.products_record_for_admin_url + exist_product_id, format="json", follow=True)
        self.assertEqual(res.status_code, 200)
        # pdb.set_trace()
    
    def test_exist_single_record_products_with_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        exist_product_id = '200'
        res = self.client.get(self.products_record_for_admin_url + exist_product_id, format="json", follow=True)
        self.assertEqual(res.status_code, 403)
        # pdb.set_trace()

    def test_not_exist_single_record_products(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        not_exist_product_id = '10001'
        res = self.client.get(self.products_record_for_admin_url + not_exist_product_id, format="json", follow=True)
        self.assertEqual(res.status_code, 404)
        # pdb.set_trace()
    
    def test_update_single_record_products(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        exist_product_id = '200'
        updated_data = {
            "name": "string updated",
            "description": "string updated",
            "price_eur": 30
        }
        res = self.client.put(self.products_update_for_admin_url + exist_product_id, updated_data, format="json", follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['data']['price_eur'], updated_data['price_eur'])
        self.assertEqual(res.data['data']['description'], updated_data['description'])
    
    def test_update_single_record_products_with_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        exist_product_id = '200'
        updated_data = {
            "name": "string updated",
            "description": "string updated",
            "price_eur": 30
        }
        res = self.client.put(self.products_update_for_admin_url + exist_product_id, updated_data, format="json", follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 403)
       
    
    def test_delete_exist_single_record_products(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        exist_product_id = '200'
        res = self.client.delete(self.products_delete_for_admin_url + exist_product_id, follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 201)
    
    def test_delete_exist_single_record_products_with_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        exist_product_id = '200'
        res = self.client.delete(self.products_delete_for_admin_url + exist_product_id, follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 403)
    
    def test_delete_not_exist_single_record_products(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        exist_product_id = '1001'
        res = self.client.delete(self.products_delete_for_admin_url + exist_product_id, follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 404)

    def test_integrate_create_and_get_created_record(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        res = self.client.post(self.products_create_for_admin_url, self.valid_product_data, format="json", follow=True)
        self.assertEqual(res.status_code, 201)
        res = self.client.get(self.products_record_for_admin_url + str(self.valid_product_data['id']), format="json", follow=True)
        self.assertEqual(res.status_code, 200)
    
    def test_integrate_create_and_get_all_records(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        res = self.client.post(self.products_create_for_admin_url, self.valid_product_data, format="json", follow=True)
        self.assertEqual(res.status_code, 201)
        res = self.client.get(self.products_records_for_admin_url, format="json", follow=True)
        self.assertEqual(res.status_code, 200)
        #new record created so i increase length of previous created by 1
        self.assertEqual(res.data['meta']['total'], len(self.test_bulk_products) + 1)  
        self.assertEqual(len(res.data['data']), len(self.test_bulk_products) + 1)

    def test_purchase_product_for_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        purchase_product_id = {
            "product_id": 200
        }
        res = self.client.post(self.purchase_product_for_user_url, purchase_product_id, format="json", follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 201)
    
    def test_purchase_not_exist_product_for_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        purchase_product_id = {
            "product_id": 1001
        }
        res = self.client.post(self.purchase_product_for_user_url, purchase_product_id, format="json", follow=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 422)
    
    def test_integrate_purchase_and_get_purchased_products(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        purchase_product_id = {
            "product_id": 200
        }
        res = self.client.post(self.purchase_product_for_user_url, purchase_product_id, format="json", follow=True)
        self.assertEqual(res.status_code, 201)
        res = self.client.get(self.products_purchased_records_for_user_url + 'EGP', format="json", follow=True)
        self.assertEqual(res.status_code, 200)
        # puchase single product
        self.assertEqual(len(res.data['data']), 1)
        self.assertEqual(res.data['meta']['total'], 1)
    
    def test_currancy_get_all_products_records_for_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        res = self.client.get(self.products_records_for_user_url + 'EGP', follow=True)
        self.assertEqual(res.status_code, 200)
        
        # test EUR-EGP currancy conversion 
        self.assertEqual("{:.2f}".format(res.data['data'][0]['user_currancy_price']), "{:.2f}".format(res.data['data'][0]['price_eur']*18.798164))
        self.assertEqual("{:.2f}".format(res.data['data'][1]['user_currancy_price']), "{:.2f}".format(res.data['data'][1]['price_eur']*18.798164))
        self.assertEqual("{:.2f}".format(res.data['data'][2]['user_currancy_price']), "{:.2f}".format(res.data['data'][2]['price_eur']*18.798164))
        res = self.client.get(self.products_records_for_user_url + 'AED', follow=True)
        self.assertEqual(res.status_code, 200)
        # test EUR-AED currancy conversion
        self.assertEqual("{:.2f}".format(res.data['data'][0]['user_currancy_price']), "{:.2f}".format(res.data['data'][0]['price_eur']*4.401215))
        self.assertEqual("{:.2f}".format(res.data['data'][1]['user_currancy_price']), "{:.2f}".format(res.data['data'][1]['price_eur']*4.401215))
        self.assertEqual("{:.2f}".format(res.data['data'][2]['user_currancy_price']), "{:.2f}".format(res.data['data'][2]['price_eur']*4.401215))

    def test_integrate_purchase_and_get_revenue(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user_token)
        # purchase product 
        purchase_product_id = {
            "product_id": 200
        }
        res = self.client.post(self.purchase_product_for_user_url, purchase_product_id, format="json", follow=True)
        self.assertEqual(res.status_code, 201)
        purchase_product_id = {
            "product_id": 201
        }
        res = self.client.post(self.purchase_product_for_user_url, purchase_product_id, format="json", follow=True)
        self.assertEqual(res.status_code, 201)
        # get revenue 
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.admin_token)
        res = self.client.get(self.products_revenue_for_admin_url, follow=True)
        # pdb.set_trace()
        self.assertEqual(res.data['data']['total_revenue_eur'], self.test_prices[0]+self.test_prices[1])
        