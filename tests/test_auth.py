from tests.base import BaseTestCase
from flask import url_for

class AuthTestCase(BaseTestCase):
    def test_login(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertIn('Welcome back!', data)
    
    def test_fail_login(self):
        response = self.login(username='aaa', password='bbb')
        data = response.get_data(as_text=True)
        self.assertIn('Invalid username or password.', data)

    def test_logout(self):
        self.login()  #注意要先登陆
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('Logout success!', data)
    
    def test_admin_protect(self):
        response = self.client.get(url_for('admin.settings'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Please log in to access this page.', data)