#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: initilize and create application instance by factory mode

# add flask and render template support
from flask import Flask, render_template

# add bootstrap support
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()

# add moment support
from flask_moment import Moment
moment = Moment()

# add database support
from flask_sqlalchemy import SQLAlchemy
database = SQLAlchemy()

# add mail support
from flask_mail import Mail
mail = Mail()

# add login support
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# add config
from config import config

# create application instance
def create_application(config_name):
    application = Flask(__name__)

    # init application by configuration
    application.config.from_object(config[config_name]())

    # init application by bootstrap
    bootstrap.init_app(application)

    # init application by moment
    moment.init_app(application)

    # init application by database
    database.init_app(application)

    # init application by mail
    mail.init_app(application)

    # inir application by login manager
    login_manager.init_app(application)

    # init application by other module

    # register main blueprint
    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    # register auth blueprint, and add url_prefix
    from .auth import auth as auth_blueprint
    application.register_blueprint(auth_blueprint, url_prefix='/auth')

    # return application instance
    return application
