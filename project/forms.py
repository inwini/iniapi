
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    website = StringField(
        'Website',
        validators=[Optional()]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SearchForm(FlaskForm):
    build_name = StringField('Build Name', validators=[DataRequired()])
    date_start = DateField('Date Start', validators=[DataRequired()])
    date_end = DateField('Date End', validators=[DataRequired(), Email()])
    time_start = TimeField('Time Start', validators=[DataRequired()])
    time_end = TimeField('Time End', validators=[DataRequired()])