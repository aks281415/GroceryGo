from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FloatField , DateField
from wtforms.validators import ValidationError, Email, EqualTo, Length, InputRequired 
from model import User


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=30, message='Should be less than 30 characters')])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')


    

