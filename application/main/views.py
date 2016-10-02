#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: blueprint form views handlers

# define route / views
from . import main
from .forms import NameForm
from .. import database
from ..models import User
#from ..mails import send_mail
from datetime import datetime
from flask import render_template, redirect, url_for, session
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(user_name=form.name.data).first()
        if user is None:
            user=User(user_name=form.name.data)
            database.session.add(user)
            session['known']=False
            #send_mail('pengqiang5@asiainfo.com', 'New User', 'mail/new_user', name=form.name.data)
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name',None), known=session.get('known', False))

