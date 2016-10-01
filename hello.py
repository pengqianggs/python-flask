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

# add sqlalchemy support
import os
from flask_sqlalchemy import SQLAlchemy
basedir=os.path.abspath(os.path.dirname(__file__))
application.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'data.sqlite')
application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(application)
class Role(db.Model):
    __tablename__='role'
    role_id=db.Column(db.Integer, primary_key=True)
    role_name=db.Column(db.String(32), unique=True)

    def __repr__(self):
        return 'role <%r>' % self.role_name

class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(32), unique=True, index=True)
    role_id=db.Column(db.Integer, index=True)

    def __repr__(self):
        return 'user <%r>' % self.user_name

# create db table
db.create_all()

# add python shell support
from flask_script import Shell
def make_shell_context():
    return dict(application=application, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))

# add python migrate support
from flask_migrate import Migrate, MigrateCommand
migrate=Migrate(application, db)
manager.add_command('db', MigrateCommand)

# add mail support
from flask_mail import Mail, Message
application.config['MAIL_SERVER']=os.environ.get('MAIL_SERVER')
application.config['MAIL_PORT']=os.environ.get('MAIL_PORT')
application.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
application.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
application.config['MAIL_USE_SSL']=os.environ.get('MAIL_USE_SSL', False)
application.config['MAIL_USE_TLS']=os.environ.get('MAIL_USE_TLS', False)
application.config['MAIL_SENDER']=os.environ.get('MAIL_SENDER')
mail = Mail(application)

def send_mail(to, subject, template, **kwargs):
    message=Message(subject, sender=application.config['MAIL_SENDER'], recipients=[to])
    message.body=render_template(template+'.txt', **kwargs)
    message.html=render_template(template+'.html', **kwargs)
    mail.send(message)

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
        user=User.query.filter_by(user_name=form.name.data).first()
        if user is None:
            user=User(user_name=form.name.data)
            db.session.add(user)
            session['known']=False
            send_mail('pengqiang5@asiainfo.com', 'New User', 'mail/new_user', name=form.name.data)
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name', None), known=session.get('known', False))

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
