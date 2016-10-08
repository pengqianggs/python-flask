#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: Set all configurations

import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'learning python flask'
    SQLALCHEMY_COMMIT_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or 'Python.Flask'
    MAIL_SENDER = os.environ.get('MAIL_SENDER') or '834506701@qq.com'

    @staticmethod
    def init_app(self, application):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '834506701'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'gkawlcljvrogbchc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
    }

