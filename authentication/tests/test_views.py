from .test_setup import TestSetUp
import pdb
from ..models import User

class TestViews(TestSetUp):
   
   
    """"""""""""""""""""""""""""""""""""""""""
    # super user testing
    """"""""""""""""""""""""""""""""""""""""""
    def test_super_user(self):
        password = 'mypassword' 
        email    = 'myemail@test.com'
        username = 'admin'
        User.items.create_superuser(email, password, **{'username': username})
        admin_credential = {
            "username": username,
            "password": password
        }
        res = self.client.post(self.login_url, admin_credential, format="json")
        self.assertEqual(res.status_code, 201)
    """"""""""""""""""""""""""""""""""""""""""
    # sing up testing 
    """"""""""""""""""""""""""""""""""""""""""

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.signup_url)
        self.assertEqual(res.status_code, 422)
    
    def test_user_cannot_register_with_invalid_password(self):
        res = self.client.post(self.signup_url, self.user_data_invalid_password, format="json")
        self.assertEqual(res.status_code, 422)
        
    def test_user_cannot_register_with_invalid_email(self):
        res = self.client.post(self.signup_url, self.user_data_invalid_email, format="json")
        self.assertEqual(res.status_code, 422)
    
    def test_user_cannot_register_with_incomplete_data(self):
        # remove attributes form entered data and test the api without it 
        # remove email 
        temp = self.user_data_valid 
        self.user_data_valid.pop('email')
        res = self.client.post(self.signup_url, self.user_data_valid, format="json")
        self.assertEqual(res.status_code, 422)
        # remove username 
        self.user_data_valid = temp 
        self.user_data_valid.pop('username')
        res = self.client.post(self.signup_url, self.user_data_valid, format="json")
        self.assertEqual(res.status_code, 422)
        # remove last_name  
        self.user_data_valid = temp 
        self.user_data_valid.pop('last_name')
        res = self.client.post(self.signup_url, self.user_data_valid, format="json")
        self.assertEqual(res.status_code, 422)
        # remove password  
        self.user_data_valid = temp 
        self.user_data_valid.pop('password')
        res = self.client.post(self.signup_url, self.user_data_valid, format="json")
        self.assertEqual(res.status_code, 422)

    def test_user_can_register_and_login_correctly(self):
        res = self.client.post(self.signup_url, self.user_data_valid, format="json")
        # pdb.set_trace()
        self.assertEqual(res.data['data']['user']['email'], self.user_data_valid['email'])
        self.assertEqual(res.data['data']['user']['username'], self.user_data_valid['username'])
        self.assertEqual(res.status_code, 201)

        res = self.client.post(self.login_url, self.user_data_valid, format="json")
        self.assertEqual(res.status_code, 201)
        
    """"""""""""""""""""""""""""""""""""""""""
    # login testing 
    """"""""""""""""""""""""""""""""""""""""""
    
    def test_user_can_login_with_no_data(self):
        res = self.client.post(self.login_url, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 400)
    
    def test_user_can_login_with_no_password(self):
        # remove password  
        self.user_data_valid.pop('password')
        res = self.client.post(self.login_url, self.user_data_valid, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 400)

