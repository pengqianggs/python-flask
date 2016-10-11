#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: module main initialize as blueprint

# define a blueprint main
from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors

# register permission into context
from ..models import Permission
@main.app_context_processor
def register_permission():
    return dict(Permission=Permission)
