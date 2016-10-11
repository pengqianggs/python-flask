#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: define main blueprint forms

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import Length, EqualTo

# define edit profile form
class EditProfileForm(FlaskForm):
    realname=StringField('Realname', validators=[Length(0, 64)])
    location=StringField('Location', validators=[Length(0, 64)])
    aboutme=TextAreaField('About Me')
    submit=SubmitField('Modify')

# define change password from
class ChangePasswordForm(FlaskForm):
    old_password=PasswordField('Old Password')
    new_password=PasswordField('New Password')
    confirm_password=PasswordField('Confirm Password', validators=[EqualTo('new_password')])
    submit=SubmitField('Modify')

