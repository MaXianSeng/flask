from dotenv import load_dotenv
import os
from werkzeug.contrib.fixers import ProxyFix #反向代理

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path) #手动导入环境变量

from bluelog import create_app

app = create_app('production')
app.wsgi_app = ProxyFix(app.wsgi_app)#方向代理设置