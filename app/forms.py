""" Gives ability to make Log in and Create Account forms""" 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """ 
    A form for users to fill out in order to Log in 
    """
    username = StringField('Username', validators=[DataRequired()]) #This is the form for username
    password = PasswordField('Password', validators=[DataRequired()]) #This is the form for passwords
    remember_me = BooleanField('Remember Me') #This is the box for "Remember Me" option
    submit = SubmitField('Sign In') 