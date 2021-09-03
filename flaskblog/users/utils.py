from flask_mail import Message
from flask import url_for, current_app as app
from flaskblog import mail
from PIL import Image
import secrets
import os

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)

    output_size = (150,150)
    i= Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    #form_picture.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Reset Password',
                 sender='no-reply@domail.com', recipients=[user.email])
    msg.body = f'''Please go to the following page and choose a new password:
<a href="{url_for('reset_token', token=token, _external=True) }">Click here</a>
Your username, in case you’ve forgotten:{user.username }
Thanks for using our site!
'''
    mail.send(msg)