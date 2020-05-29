from flask import Flask, current_app
from bluelog.settings import config
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.blueprints.admin import admin_bp
from bluelog.extensions import bootstrap, db, moment, ckeditor, mail, login_manager, csrf#, cache, toolbar, migrate
import os
import click
from flask_sqlalchemy import get_debug_queries
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name=None):  #当使用flask run启动程序时，此函数会自动被调用执行
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_template_context(app)
    register_request_handlers(app)
    register_logging(app) #程序日志
    return app

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    #toolbar.init_app(app) #调试调程序工具
    #cache.init_app(app) #缓存
    #migrate.init_app(app, db) #迁移工具

def register_logging(app):  #程序日志
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'), #低等级日志写入文件
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Bluelog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR) #高等级日志通过邮件发送给开发人员
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)

def register_blueprints(app): #注册蓝本
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(admin_bp, url_prefix='/admin')

def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=200, help='Quantity of comments, default is 240.')

    def  forge(category, post, comment):
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')
    
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option( 
        '--password', prompt=True, hide_input=True,
        confirmation_prompt=True, help='The password used to login.'
     )
    def init(username, password):
        click.echo('Initializing the database...')
        db.create_all()

        admin = My_Admin.query.first()
        if admin:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = My_Admin( 
                username = username,
                blog_title = 'Bluelog',
                blog_sub_title = "Reality is the only thing real.",
                name = 'Admin',
                about = "Anything about you."
             )
            admin.set_password(password)
            db.session.add(admin)
            db.commit()
            click.echo('Done')

from bluelog.models import My_Admin, Category, Post, Comment

#def register_shell_context(app):
    #@app.shell_context_processor
    #def make_shell_context():
        #return dict(db=db, My_Admin=My_Admin, Post=Post, Category=Category, Comment=Comment)

def register_template_context(app): #模板上下文处理函数，在渲染模板时会自动执行app.context_processor修饰的函数
    @app.context_processor          #这样所有的模板都可以直接使用admin和categories了
    def make_template_context():
        admin = My_Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)

def register_request_handlers(app):  #记录数据库慢查询
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= current_app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
                current_app.logger.warning( 
                    'Slow query: Duration: %fs/n Context: %s/n Query: %s/n'
                    %(q.duration, q.context, q.statement)
                 )
        return response