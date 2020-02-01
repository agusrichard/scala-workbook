from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User 
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, \
					PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm


@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()


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
		flash('Invalid email or password.', 'warning')
	return render_template('auth/login.html', title='Login', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.', 'info')
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
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Account',
					'auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to you by email.', 'info')
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
				'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.', 'info')
	return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			db.session.commit()
			flash('Your password has been updated', 'success')
		else:
			flash('Invalid password', 'warning')
	return render_template('auth/change_password.html', title='Change Password', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email, 'Reset Your Password', 'auth/email/reset_password',
						user=user, token=token)
		flash('An email with instructions to reset your password has been sent to you.', 'info')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_request.html', title='Request Reset Password', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		if User.reset_password(token, form.password.data):
			db.session.commit()
			flash('Your password has been updated.', 'success')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html', title='Reset Password', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			new_email = form.email.data.lower()
			token = current_user.generate_email_change_token(new_email)
			send_email(new_email, 'Confirm your email address',
						'auth/email/change_email', user=current_user, token=token)
			flash('An email with instructions to confirm your new email '
					'address has been sent to you.', 'info')
			return redirect(url_for('main.index'))
		else:
			flash('Invalid email or password', 'warning')
	return render_template('auth/change_email.html', title='Change Email', form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
	if current_user.change_email(token):
		db.session.commit()
		flash('Your email address has been updated.', 'success')
	else:
		flash('Invalid request.')
	return redirect(url_for('main.index'))