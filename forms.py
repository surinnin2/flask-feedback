from werkzeug.utils import validate_arguments
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20, message='Username must be between 1-20 characters')])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Length(max=50, message='Email cannot exceed 50 characters')])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=30, message='First Name cannot exceed 20 characters')])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=30, message='Last Name cannot exceed 20 characters')])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=1, max=100, message='Title cannot exceed 100 characters')])
    content = StringField('Content', validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20, message='Username must be between 1-20 characters')])
    password = PasswordField('Password', validators=[InputRequired()])
