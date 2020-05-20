from tests.base import BaseTestCase
from bluelog.models import Post, Category, Comment
from bluelog.extensions import db
from flask import url_for

#由于每个测试模块测试的功能都不一样，所以最好在每个测试模块都定义一个setUp()，并且继承基础的setUp()
#模块间的setUp()好像不可以直接使用，这几个程序都继承了基类
class BlogTestCase(BaseTestCase):
    def setUp(self):
        super(BlogTestCase, self).setUp()
        self.login()

        category = Category(name='Default')
        post = Post(title='This is a test', body='A simple test.', category=category)
        comment = Comment(body='A comment', post=post, from_admin=True, reviewed=True)

        db.session.add(category)
        db.session.add(post)
        db.session.add(comment)
        db.session.commit()
    
    def test_index_page(self):
        response = self.client.get('/blog/')
        data = response.get_data(as_text=True)

        self.assertIn('Home', data)
        self.assertIn('It is a test', data)
        self.assertIn('Test', data)
        self.assertIn('This is a test', data)
        self.assertIn('Default', data)
    
    def test_about(self):
        response = self.client.get('/blog/about')
        data = response.get_data(as_text=True)
        self.assertIn('About', data)
        self.assertIn('Test this programme', data)
    
    def test_show_category(self):
        response = self.client.get(url_for('blog.show_category', category_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('Default', data)
        self.assertIn('This is a test', data)
    
    def test_show_post(self):
        response = self.client.get(url_for('blog.show_post', post_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('A simple test.', data)
        self.assertIn('Default', data)
        self.assertIn('A comment', data)
    
    def test_new_comment(self):
        response = self.client.post(url_for('blog.show_post', post_id=1), data=dict( 
            author = 'author',
            email = 'email',
            site = 'site',
            body = 'I am a comment',
            post = Post.query.get(1)  #注意，需要写在这个地方，作为数据一起提交
         ), follow_redirects=True)
        data = response.get_data(as_text=True)
        #self.assertIn('Comment success', data)
        self.assertIn('I am a comment', data) #按照程序reviewed=False那么data中应该没有此评论才对，不懂
    
    def test_new_reply(self):
        response = self.client.post(url_for('blog.show_post', post_id=1) + '?reply_to=1', data=dict( #此处是测试评论评论，需要特别注意
            author = 'author2',
            email = 'email2',
            site = 'site2',
            body = 'I reply a comment',
            post = Post.query.get(1)
         ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('I reply a comment', data)
    
    def test_change_theme(self):
        response = self.client.get(url_for('blog.change_theme', theme_name='perfect_blue'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('css/perfect_blue.min.css', data)
        self.assertNotIn('css/black_swan.min.css', data)

        response = self.client.get(url_for('blog.change_theme', theme_name='black_swan'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('css/black_swan.min.css', data)
        self.assertNotIn('css/perfect_blue.min.css', data)