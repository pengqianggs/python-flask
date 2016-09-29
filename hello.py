#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: This is a test python program.

from flask import Flask
from flask.ext.script import Manager

application = Flask(__name__)

# init application use manager
manager = Manager(application);

# index view process
@application.route('/')
def index():
    return '<h1>Hello Flask!</h1>'

# view process with parameters
@application.route('/<username>')
def userinfo(username):
    return '<h1>Welcome %s back!</h1>' % username

if __name__ == '__main__':
    manager.run()
