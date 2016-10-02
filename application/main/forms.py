#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: define main blueprint forms

# define NameForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name=StringField('what is your name?', validators=[Required()])
    submit=SubmitField('Submit')
