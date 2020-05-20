from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Optional, URL
from flask_ckeditor import CKEditorField
from bluelog.models import Category

class LoginForm(FlaskForm):  #登录表单
    username = StringField('Username', validators=[DataRequired(), Length(1,20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1,60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [ 
            ( category.id, category.name ) for category in Category.query.order_by(Category.name).all()
         ]

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1,30)])
    submit = SubmitField('Submit')
    
    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')

class CommentForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(1,30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1,254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0,255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AdminCommentForm(CommentForm):#管理员评论的表单
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()

class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 30)])
    blog_sub_title = StringField('Blog Subtitle', validators=[DataRequired(), Length(1, 128)])
    about = TextAreaField('About', validators=[DataRequired()])
    submit = SubmitField('Submit')