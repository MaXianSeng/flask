#实例化扩展
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
#from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache  #缓存
#from flask_migrate import Migrate  #迁移工具

bootstrap = Bootstrap()
ckeditor = CKEditor()
mail = Mail()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
csrf = CSRFProtect()
#toolbar = DebugToolbarExtension() #使用扩展Flask-DebugToolbar调试程序
cache = Cache()
#migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import My_Admin
    user = My_Admin.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'