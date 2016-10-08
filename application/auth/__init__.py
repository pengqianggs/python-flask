#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: create author blueprint

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
