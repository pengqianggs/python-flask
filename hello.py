#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: This is a test python program.

# init application by flask
from flask import Flask
application = Flask(__name__)
application.config['SECRET_KEY']='learning flask'

# init application by manager
from flask_script import Manager
manager = Manager(application);

# init application by bootstrap
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(application)

# init application by moment
from flask_moment import Moment
moment = Moment(application)

# add form support 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
class NameForm(FlaskForm):
    name=StringField('what is your name?', validators=[Required()])
    submit=SubmitField('Submit')

# index view process
from flask import render_template, session, redirect, url_for, flash
from datetime import datetime
@application.route('/', methods=['GET', 'POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        old_name=session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('name already changed!')
        session['name']=form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', name=session.get('name'), form=form)

# view process with parameters
@application.route('/<username>')
def userinfo(username):
    return render_template('user.html', name=username)

# error 404 handler
@application.errorhandler(404)
def page_not_found(ex):
    return render_template('404.html'), 404

# error 500 hander
@application.errorhandler(500)
def internal_server_error(ex):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
