#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: blueprint form views handlers

from flask import render_template, abort, redirect, url_for, flash
from ..models import User
from flask_login import current_user, login_required, logout_user
from .. import database
from .forms import EditProfileForm, ChangePasswordForm

# define route / views
from . import main
@main.route('/')
def index():
    return render_template('index.html')

# user info view
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

# edit user profile view
@main.route('/user/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.realname = form.realname.data
        current_user.location = form.location.data
        current_user.aboutme = form.aboutme.data
        database.session.add(current_user)
        database.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('main.user', username=current_user.name))
    form.realname.data = current_user.realname
    form.location.data = current_user.location
    form.aboutme.data = current_user.aboutme
    return render_template('edit-profile.html', form=form)

# change password view
@main.route('/user/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form=ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('old password is invalid')
            return render_template('change-password.html', form=form)
        if form.old_password.data == form.new_password.data:
            flash('old password same as new password')
            return render_template('change-password.html', form=form)
        if form.new_password.data != form.confirm_password.data:
            flash('new password does not equal to comfirm password')
            return render_template('change-password.html', form=form)
        current_user.set_password(form.confirm_password.data)
        database.session.add(current_user)
        database.session.commit()
        flash('change password successfully, please login use new password')
        return redirect(url_for('auth.logout'))
    form.old_password.data = ''
    form.new_password.data = ''
    form.confirm_password.data = ''
    return render_template('change-password.html', form=form)

