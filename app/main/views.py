from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask_login import login_required, current_user, login_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from ..auth.forms import LoginForm
from .. import db
from ..models import Permission, Role, User, Post
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			next = request.args.get('next')
			if next is None or not next.startswith('/'):
				next = url_for('main.home')
			return redirect(next)
		flash('Invalid email or password', 'warning')
	return render_template('index.html', index_page=True, form=form)


@main.route('/home', methods=['GET', 'POST'])
def home():
	form = PostForm()
	if current_user.can(Permission.WRITE) and form.validate_on_submit():
		post = Post(body=form.body.data,
					author=current_user._get_current_object())
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('main.home'))
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
			page, per_page=current_app.config['TALOS_POSTS_PER_PAGE'],
			error_out=False)
	posts = pagination.items
	return render_template('main/home.html', form=form, posts=posts, pagination=pagination, title='Home')


@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
			page, per_page=current_app.config['TALOS_POSTS_PER_PAGE'],
			error_out=False)
	posts = pagination.items
	return render_template('main/user.html', user=user, posts=posts, pagination=pagination, title=user.username)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user._get_current_object())
		db.session.commit()
		flash('Your profile has been updated.', 'success')
		return redirect(url_for('main.user', username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('main/edit_profile.html', title='Edit Profile', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username = form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		user.about_me = form.about_me.data
		db.session.add(user)
		db.session.commit()
		flash('The profile has been updated.', 'success')
		return redirect(url_for('main.user', username=user.username))
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me.data = user.about_me
	return render_template('main/edit_profile_admin.html', title='Admin Edit Profile', user=user, form=form)


@main.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('main/post.html', posts=[post], title="Post {}".format(id))


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and \
			not current_user.can(Permission.ADMIN):
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		db.session.commit()
		flash('The post has been updated.', 'success')
		return redirect(url_for('main.user', username=post.author.username))
	form.body.data = post.body
	return render_template('main/edit_post.html', form=form, title='Edit Post')