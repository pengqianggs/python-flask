#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: all mails of all blueprints handlers

from . import mail
from flask_mail import Message
from flask import current_app, render_template

# send mail sync
def send_mail(to, subject, template, **kwargs):
    message=Message(subject, sender=current_app.config['MAIL_SENDER'], recipients=[to])
    message.body=render_template(template+'.txt', **kwargs)
    message.html=render_template(template+'.html', **kwargs)
    mail.send(message)

# send mail async
from threading import Thread
def send_async_mail(to, subject, template, **kwargs):
    pass
