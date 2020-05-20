from tests.base import BaseTestCase
from flask import url_for
from bluelog.models import Post, Comment, Category
from bluelog.extensions import db

class AdminTestCase(BaseTestCase):
    def setUp(self):
        super(AdminTestCase, self).setUp()
        self.login()

        category = Category(name='Default')
        post = Post(title='This is a admin test', body='A simple admin test.', category=category)
        comment_1 = Comment(body='A admin comment1', post=post, from_admin=True, reviewed=True)
        comment_2 = Comment(body='A admin comment2', post=post, from_admin=False, reviewed=False)
        comment_3 = Comment(body='A admin comment3', post=post, from_admin=False, reviewed=False)
        db.session.add_all([category, post, comment_1, comment_2, comment_3])
        db.session.commit()

    def test_settings(self):
        response = self.client.get(url_for('admin.settings'))
        data = response.get_data(as_text=True)
        self.assertIn('It is a test', data)

        response = self.client.post(url_for('admin.settings'), data=dict( 
            name = 'Xue Wu',
            blog_title = 'Xue Wu test',
            blog_sub_title = '2nd test',
            about = '2nd about'
         ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Setting updated!', data)
        self.assertIn('Xue Wu test', data)
    
    def test_new_post(self):
        response = self.client.post(url_for('admin.new_post'), data=dict( 
            title = 'a admin post',
            category = 1,
            body = 'i am a admin post'
         ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Post created!', data)
        self.assertIn('a admin post', data)
        self.assertIn('i am a admin post', data)
        
    def test_edit_post(self):
        response = self.client.get(url_for('admin.edit_post', post_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('Edit Post', data)


        response = self.client.post(url_for('admin.edit_post', post_id=1), data=dict( 
            title = 'edit a admin post',
            category = 1,
            body = 'edit i am a admin post'
         ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Edit post success!', data)
        self.assertIn('edit a admin post', data)
        self.assertIn('edit i am a admin post', data)
        
    def test_manage_post(self):
        response = self.client.get(url_for('admin.manage_post'))
        data = response.get_data(as_text=True)
        self.assertIn('1', data)
        self.assertIn('Manage Posts', data)
    
    def test_delete_post(self):
        response = self.client.get(url_for('admin.delete_post', post_id=1), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Post deleted!', data)
        self.assertIn('405 Method Not Allowed', data)

        response = self.client.post(url_for('admin.delete_post', post_id=1), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(Post.query.get(1) is None)
        self.assertIn('Post deleted!', data)
    
    def test_approve_comment(self): 
        response = self.client.post(url_for('admin.approve_comment', comment_id=2), follow_redirects=True)
        data = response.get_data(as_text=True)
        comment = Comment.query.get(2)
        self.assertIn('Comment published!', data)
        self.assertTrue(comment.reviewed is True)
    
    def test_manage_comment(self):
        response = self.client.get(url_for('admin.manage_comment', filter='admin'))
        data = response.get_data(as_text=True)
        self.assertIn('A admin comment1', data)
        self.assertIn('1', data)

        response = self.client.get(url_for('admin.manage_comment', filter='unread'))
        data = response.get_data(as_text=True)
        self.assertIn('A admin comment2', data)
        self.assertIn('A admin comment3', data)
        self.assertTrue('2', data)

        response = self.client.get(url_for('admin.manage_comment'))
        data = response.get_data(as_text=True)
        self.assertIn('A admin comment1', data)
        self.assertIn('A admin comment2', data)
        self.assertIn('A admin comment3', data)
        self.assertTrue('3', data)

    def test_delete_comment(self):
        response = self.client.post(url_for('admin.delete_comment', comment_id=3), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Comment deleted!', data)
        self.assertTrue(Comment.query.get(3) is None)