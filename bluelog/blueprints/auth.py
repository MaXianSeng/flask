from flask import Blueprint, render_template, redirect, url_for, flash
from bluelog.forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from bluelog.utils import redirect_back
from bluelog.models import My_Admin

auth_bp = Blueprint('auth', __name__)  #创建蓝本

#装配蓝本，注册操作
@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit:
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = My_Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password): #验证用户名和密码
                login_user(admin, remember) #登入用户
                flash('Welcome back!', 'info')
                return redirect_back() #返回上一个页面
            flash('Invalid username or password.', 'warning') #用户名或密码错误
        else:
            flash('No account!', 'warning')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required #需要先登录
def logout():
    logout_user()
    flash('Logout success!', 'info')
    return redirect_back()
