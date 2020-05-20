from bluelog.models import My_Admin, Category, Post, Comment
from bluelog.extensions import db
from faker import Faker
import random
from sqlalchemy.exc import IntegrityError

fake = Faker()

def fake_admin():
    admin = My_Admin( 
        username = 'MXD',
        blog_title = 'Bluelog',
        blog_sub_title = 'Reality is the only thing real.',
        name = 'Aobama',
        about = 'Ready Player No.1'
     )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()

def fake_categories(count=10):
    category = Category(name='Default') #首先创建一个默认分类
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError: #分类名不可重复
            db.session.rollback()

def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title  = fake.sentence(),
            body = fake.text(300),
            category = Category.query.get(random.randint(1, Category.query.count())),
            timestamp = fake.date_time_this_year()
         )
        db.session.add(post)
    db.session.commit()

def fake_comments(count=200):
    for i in range(count):
        comment = Comment( 
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = True,   #审核过的评论
            post = Post.query.get(random.randint(1, Post.query.count()))
         )
        db.session.add(comment)
    
    for i in range(int(count * 0.05)):
        comment = Comment( 
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = False,   #未审核过的评论
            post = Post.query.get(random.randint(1, Post.query.count()))
         )
        db.session.add(comment)

    for i in range(int(count * 0.05)):#来自管理员的评论
        comment = Comment( 
            author = 'MXD',
            email = 'MXD@qq.com',
            site = 'www.MXD.com',
            body = 'Good comment!',
            timestamp = fake.date_time_this_year(),
            from_admin = True,
            reviewed = True,
            post = Post.query.get(random.randint(1, Post.query.count()))
         )
        db.session.add(comment)
    
    db.session.commit()

    for i in range(int(count * 0.1)): #评论的回复
        comment = Comment( 
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = True,   #审核过的评论
            replied = Comment.query.get(random.randint(1, Comment.query.count())),
            post = Post.query.get(random.randint(1, Post.query.count()))
         )
        db.session.add(comment)
    db.session.commit()