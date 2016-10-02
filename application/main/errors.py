#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: blueprint main errors handlers

from . import main
from flask import render_template

@main.errorhandler(404)
def page_not_found(ex):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(ex):
    return render_template('500.html'), 500

