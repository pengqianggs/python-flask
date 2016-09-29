#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: This is a test python program.

from flask import Flask
from flask.ext.script import Manager
from flask import render_template
from flask.ext.bootstrap import Bootstrap

application = Flask(__name__)

# init application by manager
manager = Manager(application);

# init application by bootstrap
bootstrap = Bootstrap(application)

# index view process
@application.route('/')
def index():
    return render_template('index.html')

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
