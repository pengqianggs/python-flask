#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: create auth blueprint views

from flask import render_template, redirect, url_for, request, flash
from . import auth
from ..models import User
from ..mails import send_mail
from .. import database
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required

# register unconfirmed user intercept hook
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
                return redirect(url_for('auth.unconfirmed'))

# user unconfirmed view
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

# user login route view
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            if user is None:
                flash('User %s dose not exist!' % form.email.data)
            else:
                flash('Invalid password')
    return render_template('auth/login.html', form=form)

# user logout route view
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

# user register view
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.username.data)
        user.set_password(form.password.data)
        database.session.add(user)
        database.session.commit()
        token=user.generate_confirmation_token(expiration=600)
        send_mail(user.email, 'Confirm your account', 'auth/mail/confirm', user=user, token=token)
        flash('A confirm E-mail has sent. please check!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

# user register confirm account
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        print "after confirm, user confirmed = ", current_user.confirmed
        flash('You have confirmed your account, thanks!')
    else:
        flash('The confirm link is invalid or has expired!')
    return redirect(url_for('main.index'))

# user resend confirm email
@auth.route('/reconfirm')
@login_required
def resend_confirm():
    token=current_user.generate_confirmation_token()
    send_mail(current_user.email, 'Confirm your account', 'auth/mail/confirm', user=current_user, token=token)
    flash('A confirm E-mail has sent. please check!')
    return redirect(url_for('main.index'))

