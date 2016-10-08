#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: blueprint form views handlers

from flask import render_template

# define route / views
from . import main
@main.route('/')
def index():
    return render_template('index.html')
