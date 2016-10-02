#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: define all models in all blueprint

from . import database

# define Role model
class Role(database.Model):
    __tablename__='role'
    role_id=database.Column(database.Integer, primary_key=True)
    role_name=database.Column(database.String(32), unique=True)

    def __repr__(self):
        return 'role <%r>' % self.role_name

# define User model
class User(database.Model):
    __tablename__='user'
    user_id=database.Column(database.Integer, primary_key=True)
    user_name=database.Column(database.String(32), unique=True, index=True)
    role_id=database.Column(database.Integer, index=True)

