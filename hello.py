#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: This is a test python program.

from flask import Flask
from flask.ext.script import Manager
from flask import render_template

application = Flask(__name__)

# init application use manager
manager = Manager(application);

# index view process
@application.route('/')
def index():
    return render_template('index.html')

# view process with parameters
@application.route('/<username>')
def userinfo(username):
    return render_template('user.html', name=username)

if __name__ == '__main__':
    manager.run()
