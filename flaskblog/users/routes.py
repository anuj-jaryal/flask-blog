from flask import  render_template, url_for,flash, redirect, request, abort,Blueprint
from flaskblog.users.forms import RegistrationForm, LoginForm, UpddateAccountForm, RequestResetForm,ResetPasswordForm,ChangePasswordForm
from flaskblog.models import User,Post
from flaskblog import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
import json
from flaskblog.users.utils import save_picture, send_reset_email



users = Blueprint('users', __name__)


@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index_post'))
    form = RegistrationForm();
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = hash_pw
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created succesfully, Please Login', 'success')
        return redirect(url_for('users.login'))
    return render_template('accounts/register.html', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index_post'))
    form =LoginForm();
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('posts.index_post'))
        else:
            flash('Email or password is incorrect', 'danger')
    return render_template('accounts/login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpddateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated successfully', 'success')
        return redirect( url_for('users.account'))
        #image_file = url_for('static',filename = 'profile_pics/'+current_user.image_file)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('accounts/profile.html', form = form)



@users.route('/user/<string:username>')
@login_required
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts =Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(per_page=5,page = page)
    return render_template('posts/user_posts.html', posts=posts,user=user)





@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index_post'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has sent to your email with instructions', 'info')
        return redirect(url_for('users.login'))
    return render_template('accounts/reset_request.html', form =form)


@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.index_post'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_pw
        db.session.commit()
        flash('Password change succesfully, Please Login', 'success')
        return redirect(url_for('users.login'))
    return render_template('accounts/reset_token.html', form =form) 

@users.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hash_pw
        db.session.commit()
        flash('Password change succesfully, Please Login', 'success')
        return redirect(url_for('users.change_password'))
    return render_template('accounts/change_password.html', form =form) 
