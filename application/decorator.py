#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: custmize decorator 

from functools import wraps
from flask_login import current_user
from flask import abort
from .models import Permission

# permission required
def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorator_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)
        return decorator_function
    return decorator

# admin required
def admin_required(func):
    return permission_required(Permission.PERMISSION_ADMIN)(func)
