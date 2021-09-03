from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, TextAreaField,SelectMultipleField
from wtforms.validators import DataRequired



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tags = SelectMultipleField('Tag',validators=[DataRequired()],coerce=int)
    submit = SubmitField('Create')