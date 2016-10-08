#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: login module forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email

# login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,32), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')

# registration form
from wtforms.validators import Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class RegistrationForm(FlaskForm):
    # Username must be make up with letters, numbers, dot or underscores.
    email = StringField('Email', validators=[Required(), Length(1,32), Email()])
    username = StringField('Username', validators=[Required(), Length(1,32), Regexp('^[A-Za-z][A-Za-z0-9._]*$',
        0, 'Username must be make up with letters, numbers, dot or underscores.')])
    password = PasswordField('Password', validators=[Required()])
    password_confirm = PasswordField('Confirm Password', validators=[Required(), EqualTo('password', 
        message='Password must be match.')])
    submit = SubmitField('Register')

    # validate email
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email had been registered.')

    # validate username
    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('The username had been registered.')
