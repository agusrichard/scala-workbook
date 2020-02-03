from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
from flask_login import login_required, current_user, login_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from ..auth.forms import LoginForm
from .. import db
from ..models import Permission, Role, User, Post
from ..decorators import admin_required, permission_required


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
	show_followed = False
	if current_user.is_authenticated:
		show_followed = bool(request.cookies.get('show_followed', ''))
	if show_followed:
		query = current_user.followed_posts
	else:
		query = Post.query
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
			page, per_page=current_app.config['TALOS_POSTS_PER_PAGE'],
			error_out=False)
	posts = pagination.items
	return render_template('main/home.html', form=form, posts=posts, pagination=pagination, 
							title='Home', show_followed=show_followed)


@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
			page, per_page=current_app.config['TALOS_POSTS_PER_PAGE'],
			error_out=False)
	posts = pagination.items
	return render_template('main/user.html', user=user, posts=posts, pagination=pagination, 
							title=user.username)


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
	return render_template('main/edit_profile_admin.html', title='Admin Edit Profile', 
							user=user, form=form)


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


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.', 'warning')
		return redirect(url_for('.home'))
	if current_user.is_following(user):
		flash('You are already following this user.', 'info')
		return redirect(url_for('.user', username=username))
	current_user.follow(user)
	db.session.commit()
	flash('You are now following %s' % username, 'success')
	return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.', 'warning')
		return redirect(url_for('.home'))
	if not current_user.is_following(user):
		flash('You are not following this user.', 'info')
		return redirect(url_for('.user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash('You are not following %s anymore' % username, 'success')
	return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.home'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followers.paginate(
		page, per_page=current_app.config['TALOS_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows = [{'user': item.follower, 'timestamp': item.timestamp}
				for item in pagination.items]
	return render_template('main/followers.html', user=user, title="Followers", 
							head_title='Followers of ',
							endpoint='.followers', pagination=pagination,
							follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.home'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followed.paginate(
		page, per_page=current_app.config['TALOS_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows = [{'user': item.followed, 'timestamp': item.timestamp}
				for item in pagination.items]
	return render_template('main/followers.html', user=user, title="Followed", 
							head_title='Followers of ',
							endpoint='.followed_by', pagination=pagination,
							follows=follows)


@main.route('/all')
@login_required
def show_all():
	resp = make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed', '', max_age=30*24*60*60)
	return resp


@main.route('/followed')
@login_required
def show_followed():
	resp = make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
	return resp



