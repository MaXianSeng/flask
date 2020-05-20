from flask import Blueprint, redirect, url_for, request, current_app, render_template, flash
from flask_login import login_required, current_user
from bluelog.models import Post, Category, Comment
from bluelog.extensions import db
from bluelog.utils import redirect_back
from bluelog.forms import PostForm, SettingForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()  #调用current_user会返回一个My_Admin实例
        flash('Setting updated!', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about = current_user.about
    return render_template('admin/settings.html', form=form)

#POST
@admin_bp.route('/post/<int:post_id>/delete', methods=['Post'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect_back()

@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination = pagination,
        posts=posts)

@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)

@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data 
        post.body = form.body.data
        post.category = Category.query.get(form.category.data) #特别注意！,表单的分类字段是分类记录的id值
        db.session.commit()
        flash('Edit post success!', 'success')
        return redirect(url_for('blog.show_post', post_id=post_id))
    form.title.data = post.title
    form.category.data = post.category_id #特别注意！
    form.body.data = post.body
    return render_template('admin/edit_post.html', form=form)

#CATEGORY
@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    return '<h1>New category</h1>'

@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return '<h1>Manage cateory</h1>'

#COMMENT
@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!', 'success')
    return redirect_back()

@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)
    if filter_rule == 'unread':
        filter_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filter_comments = Comment.query.filter_by(from_admin=True)
    else:
        filter_comments = Comment.query
    pagination = filter_comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_COMMENT_PER_PAGE'])
    comments = pagination.items
    return render_template('admin/manage_comment.html', pagination = pagination,
        comments=comments)

@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment published!', 'success')
    return redirect_back()

@admin_bp.route('/set-comment')
@login_required
def set_comment():
    return '<h1>Set comment</h1>'

