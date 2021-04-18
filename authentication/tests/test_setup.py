from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
class TestSetUp(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        fake = Faker()
        valid_email = fake.email()
        username = valid_email.split('@')[0]
        last_name = fake.first_name()
        first_name = fake.last_name()

        self.user_data_valid = {
            "email": valid_email,
            "username": username,
            "last_name": last_name,
            "first_name": first_name,
            "password": "string123344"
        }
        self.user_data_invalid_password = {
            "email": fake.email(),
            "username": fake.name(),
            "last_name": fake.first_name(),
            "first_name": fake.last_name(),
            "password": "123"
        }
        self.user_data_invalid_email = {
            "email": 'invalid-email',
            "username": fake.name(),
            "last_name": fake.first_name(),
            "first_name": fake.last_name(),
            "password": "123"
        }
        
        return super().setUp()

    def tearDown(self):
        return super().tearDown()