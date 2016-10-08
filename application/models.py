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
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
class User(UserMixin, database.Model):
    __tablename__='user'
    id=database.Column(database.Integer, primary_key=True)
    name=database.Column(database.String(32), unique=True, index=True)
    email=database.Column(database.String(32), unique=True, index=True)
    password=database.Column(database.String(128))
    confirmed=database.Column(database.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_confirmation_token(self, expiration=3600):
        serial=Serializer(current_app.config['SECRET_KEY'], expiration)
        return serial.dumps({'confirm':self.id})

    def confirm(self, token):
        serial=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=serial.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed=True
        database.session.add(self)
        database.session.commit()
        return True


# callback function for login_manager to get login user
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

