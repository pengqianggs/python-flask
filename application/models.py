#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: define all models in all blueprint

from . import database
from . import login_manager

# define permissions
class Permission:
    PERMISSION_FOLLOW = 0x01
    PERMISSION_COMMENT = 0x02
    PERMISSION_ARTICLE = 0x04
    PERMISSION_MANAGE_COMMENT = 0x08
    PERMISSION_ADMIN = 0x80

# define Role model
class Role(database.Model):
    __tablename__='role'
    id=database.Column(database.Integer, primary_key=True)
    name=database.Column(database.String(32), unique=True)
    default=database.Column(database.Boolean, index=True)
    permission=database.Column(database.Integer)
    users=database.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.PERMISSION_FOLLOW | 
                Permission.PERMISSION_COMMENT |
                Permission.PERMISSION_ARTICLE, True),
            'Moderator':(Permission.PERMISSION_FOLLOW |
                Permission.PERMISSION_COMMENT |
                Permission.PERMISSION_ARTICLE |
                Permission.PERMISSION_MANAGE_COMMENT, False),
            'Admin':(0xff, False)
        }
        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
            role.permission = roles[role_name][0]
            role.default = roles[role_name][1]
            database.session.add(role)
        database.session.commit()

    def __repr__(self):
        return 'role <%s|%d>' % (self.name, self.permission)

# define User model
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
class User(UserMixin, database.Model):
    __tablename__='user'
    id=database.Column(database.Integer, primary_key=True)
    name=database.Column(database.String(32), unique=True, index=True)
    email=database.Column(database.String(32), unique=True, index=True)
    password=database.Column(database.String(128))
    role_id=database.Column(database.Integer, database.ForeignKey('role.id'))
    confirmed=database.Column(database.Boolean, default=False)
    realname=database.Column(database.String(32))
    location=database.Column(database.String(64))
    aboutme=database.Column(database.Text())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(permission=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

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

    # permission
    def can(self, permission):
        return self.role is not None and (self.role.permission & permission) == permission

    # admin
    def is_admin(self):
        return self.can(Permission.PERMISSION_ADMIN)

# anonymous user permission
class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser

# callback function for login_manager to get login user
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

