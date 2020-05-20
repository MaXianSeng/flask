from tests.base import BaseTestCase
from bluelog.extensions import db
from bluelog.models import My_Admin, Post, Category, Comment

class CliTestCase(BaseTestCase):
    def setUUp(self):
        super(CliTestCase, self).setUp()
        db.drop_all()

    def test_forge_command(self):
        result = self.runner.invoke(args=['forge'])

        self.assertEqual(My_Admin.query.count(), 1)
        self.assertEqual(My_Admin.query.first().username, 'MXD')
        self.assertIn('Generating the administrator...', result.output)

        self.assertEqual(Category.query.count(), 11)
        self.assertEqual(Category.query.first().name, 'Default')
        self.assertIn('Generating 10 categories...', result.output)

        self.assertEqual(Post.query.count(), 50)
        self.assertIn('Generating 50 posts...', result.output)

        self.assertEqual(Comment.query.count(), 240)
        self.assertIn('Generating 200 comments...', result.output)

        self.assertIn('Done', result.output)
    
    def test_forge_command_with_count(self):
        result = self.runner.invoke(args=['forge', '--post', '60', '--comment', '100'])
        self.assertEqual(My_Admin.query.count(), 1)
        self.assertEqual(My_Admin.query.first().username, 'MXD')
        self.assertIn('Generating the administrator...', result.output)

        self.assertEqual(Category.query.count(), 11)
        self.assertEqual(Category.query.first().name, 'Default')
        self.assertIn('Generating 10 categories...', result.output)
        
        self.assertEqual(Post.query.count(), 60)
        self.assertIn('Generating 60 posts...', result.output)

        self.assertEqual(Comment.query.count(), 120)
        self.assertIn('Generating 100 comments...', result.output)

        self.assertIn('Done', result.output)