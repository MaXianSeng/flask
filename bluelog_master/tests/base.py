import unittest
from flask import url_for
from bluelog import create_app
from bluelog.extensions import db
from bluelog.models import My_Admin

class BaseTestCase(unittest.TestCase):
    #setUp()和tearDown()在每个测试方法执行前都会被执行，测试方法就是用def定义的各个函数，如def test_404_error
    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context() 
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        user = My_Admin( 
            username = 'MXD',
            blog_title = 'It is a test',
            blog_sub_title = 'Test',
            name = 'Ma',
            about = 'Test this programme'
         )
        user.set_password('123')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()
    
    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'MXD'
            password = '123'
        return self.client.post(url_for('auth.login'), data=dict( 
            username = username,
            password = password
         ), follow_redirects=True)
    
    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)