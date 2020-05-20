from bluelog.extensions import mail
from flask_mail import Message
from flask import current_app, url_for

def send_comment_mail(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    post_title = post.title
    message = Message( 
        subject='New comment',
        recipients=['2683551914 <2683551914@qq.com>'],
        sender='Xiandong Ma <%s>' %current_app.config['MAIL_USERNAME']
     )#sender这里需要特别注意！！
    message.body = 'New comment in post %s, please click %s to check.Do not reply this mail. :)'%(post_title, post_url)
    # message.html = '<p>New comment in post <i>%s</i>, click the link below to check:</p>'
    #                '<p><a href="%s">%s</a></P>'
    #                '<p><small style="color: #868e96">Do not reply this email.</small></p>'
    #                % (post.title, post_url, post_url))
    mail.send(message)