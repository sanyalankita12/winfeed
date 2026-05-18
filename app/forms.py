from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email()]
    )

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)]
    )

    confirm = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):

    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)]
    )

    submit = SubmitField('Login')


class PostForm(FlaskForm):



    content = TextAreaField(
        'Content',
        validators=[DataRequired(), Length(max=500)]
    )

    submit = SubmitField('Post')



