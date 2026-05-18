from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo,Length

class SignupForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=50)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password'),Length(min=8)])
    submit=SubmitField('Login')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])