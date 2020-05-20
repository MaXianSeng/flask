from tests.base import BaseTestCase
from flask import current_app
#from bluelog.settings import config 这个不需要

class BasicTestCase(BaseTestCase):
    def test_app_exist(self):
        self.assertFalse(current_app is None)
    
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])  #注意此处是大写的TESTING
    
    def test_404_error(self):
        response = self.client.get('/nothing') #注意此处的response和data
        data = response.get_data(as_text=True) #注意是get_data(),如果是data()会报错
        self.assertEqual(response.status_code, 404)
        self.assertIn('404 Not Found', data)