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

# add config
from config import config

# create application instance
def create_application(config_name):
    application = Flask(__name__)

    # init application by configuration
    application.config.from_object(config[config_name]())
    config[config_name].init_app(application)

    # init application by bootstrap
    bootstrap.init_app(application)

    # init application by moment
    moment.init_app(application)

    # init application by database
    database.init_app(application)

    # init application by mail
    mail.init_app(application)

    # init application by other module

    # register main blueprint
    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    # return application instance
    return application
