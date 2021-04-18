from rest_framework.test import APITestCase
from django.urls import reverse
# faker 
from faker import Faker
# models
from authentication.models import User
from ..models import Product
class TestSetUp(APITestCase):
    def setUp(self):
        login_url = reverse('login')
        signup_url = reverse('signup')
        # admins products control urls 
        self.products_create_for_admin_url = '/api/v1/product/admin/create'
        self.products_records_for_admin_url = '/api/v1/product/admin/records'
        self.products_record_for_admin_url = '/api/v1/product/admin/record/'
        self.products_delete_for_admin_url = '/api/v1/product/admin/delete/'
        self.products_update_for_admin_url = '/api/v1/product/admin/update/'
        self.products_revenue_for_admin_url = '/api/v1/product/admin/revenue'
        # user products actions url 
        self.products_records_for_user_url = '/api/v1/product/user/records/'
        self.products_purchased_records_for_user_url = '/api/v1/product/user/purchased/records/'
        self.products_record_for_user_url = '/api/v1/product/user/record/'
        self.purchase_product_for_user_url = '/api/v1/product/user/purchase'
        # fake data 
        fake = Faker()
        # admin credential 
        admin_password = 'mypassword' 
        admin_email    = fake.email()
        admin_username = admin_email.split('@')[0]
        User.items.create_superuser(admin_email, admin_password, **{'username': admin_username})
        admin_credential = {
            "username": admin_username,
            "password": admin_password
        }
        res = self.client.post(login_url, admin_credential, format="json")
        self.admin_token = res.data['data']['token'] 
        # user credential
        valid_email = fake.email()
        username = valid_email.split('@')[0]
        last_name = fake.first_name()
        first_name = fake.last_name()
        user_credential = {
            "email": valid_email,
            "username": username,
            "last_name": last_name,
            "first_name": first_name,
            "password": "string123344"
        }
        res = self.client.post(signup_url, user_credential, format="json")
        self.user_token = res.data['data']['token'] 

        # product test data 
        self.valid_product_data = {
            "id": 300,
            "name": "string",
            "description": "string",
            "price_eur": 1
        }
        
        self.invalid_price_product_data = {
            "name": "string",
            "description": "string",
            "price_eur": "string"
        }

        # products temp data and insert it in database 
        self.test_prices = [112,10,15]
        self.test_bulk_products = [
            Product(id= 200, name="product name 1 ",description="product description 1 ",price_eur=self.test_prices[0]),
            Product(id= 201,name="product name 2 ",description="product description 2 ",price_eur=self.test_prices[1]),
            Product(id= 202,name="product name 3 ",description="product description 3 ",price_eur=self.test_prices[2])
        ]
        Product.objects.bulk_create(
            self.test_bulk_products
        )
         
        return super().setUp()

    def tearDown(self):
        return super().tearDown()