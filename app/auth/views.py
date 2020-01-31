from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import db
from ..models import User 
from ..email import send_email
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			next = request.args.get('next')
			if next is None or not next.startswith('/'):
				next = url_for('main.index')
			return redirect(next)
		flash('Invalid email or password.', 'danger')
	return render_template('auth/login.html', title='Login', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.', 'success')
	return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data.lower(),
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You can now login.', 'success')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', title='Register', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		db.session.commit()
		flash('You have confirmed your account. Thanks!', 'success')
	else:
		flash('The confirmation link is invalid or has expired.', 'warning')
	return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm Your Account', 
				'auth/email/confirm', user=user, token=token)
	flash('A new confirmation email has been sent to you by email.', 'info')
	return redirect(url_for('main.index'))
