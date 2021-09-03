from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25) ])
    email = StringField('Email Address', validators= [DataRequired(), Email(), Length(min=6, max=35) ])
    password = PasswordField('Password', validators= [DataRequired(), Length(min=6, max=35) ])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password'), Length(min=6, max=35) ])
    accept_tos = BooleanField('I accept the TOS', validators=[ DataRequired() ])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators= [DataRequired(), Email(), Length(min=6, max=35) ])
    password = PasswordField('Password', validators= [DataRequired(), Length(min=6, max=35) ])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpddateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25) ])
    email = StringField('Email Address', validators= [DataRequired(), Email(), Length(min=6, max=35) ])
    picture = FileField('profile Image', validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already taken')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken')



class RequestResetForm(FlaskForm):
    email = StringField('Email Address', validators= [DataRequired(), Email(), Length(min=6, max=35) ])
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user is None:
                raise ValidationError('No account found with this email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators= [DataRequired(), Length(min=6, max=35) ])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password'), Length(min=6, max=35) ])
    submit = SubmitField('Reset password')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators= [DataRequired(), Length(min=6, max=35) ])
    password = PasswordField('Password', validators= [DataRequired(), Length(min=6, max=35) ])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password'), Length(min=6, max=35) ])
    submit = SubmitField('Change password')

    def validate_old_password(self, old_password):
        if not bcrypt.check_password_hash(current_user.password, old_password.data):
            raise ValidationError('Old password not match')