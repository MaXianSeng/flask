from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for, abort, make_response
from bluelog.models import Category, Post, Comment
from flask_login import current_user
from bluelog.forms import CommentForm
from bluelog.extensions import db# cache
from bluelog.utils import redirect_back
from bluelog.emails import send_comment_mail

blog_bp = Blueprint('blog', __name__)#创建蓝本

@blog_bp.route('/')
#@cache.cached(timeout=10 * 60)  #缓存
def index():
    page = request.args.get('page', 1, type=int) #当前请求第几页，默认为第一页
    per_page = current_app.config['BLUELOG_POST_PER_PAGE'] #每一页有几篇记录,在settings.py中
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items #当前页面的纪录列表
    return render_template('blog/index.html', pagination=pagination, posts=posts)

#@blog_bp.route('/delete-cache') #删除缓存
#def delete_cache():
#    cache.delete('view/%s' % url_for('blog.index'))
    #flash('Cached data for index have been deleted.', 'info')
#    return redirect(url_for('blog.index'))

@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/category.html', category=Category.query.get_or_404(category_id), posts=posts)

@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items

    form = CommentForm()
    from_admin = False
    reviewed = False #注意，如果为False则不会在页面中显示，因为32行规定只有为True才会显示,所以提交评论后应该在评论批准里批准为True

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment( 
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, reviewed=reviewed, post=post)

        replied_comment_id = request.args.get('reply_to')
        if replied_comment_id:
            replied_comment = Comment.query.get_or_404(replied_comment_id)
            comment.replied = replied_comment

        db.session.add(comment)
        db.session.commit()
        send_comment_mail(post) #发邮件提醒评论
        flash('Comment success', 'info')

        return redirect(url_for('blog.show_post', post_id=post_id))

    return render_template('blog/post.html', post=post, pagination=pagination,
        comments=comments, form=form)

@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('blog.show_post', post_id=comment.post_id, reply_to=comment_id,
        author=comment.author) + '#comment-form') #多余的参数用于构成查询字符串，给post.html中使用

@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)
    
    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    return response