from flask import render_template, flash, redirect, url_for
from flask import current_app as app
from application.forms import LoginForm, FarmForm, ProductForm

@app.route('/')
@app.route('/home')
def home():
	user = {'username': 'Miguel'}
	posts = [
		{
			'author': {'username': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'The Avengers movie was so cool!'
		}
	]
	return render_template('pages/home.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
			form.username.data, form.remember_me.data))
		return redirect(url_for('home'))
	return render_template('pages/login.html', title='sign In', form=form)

@app.route('/farms/create', methods=['GET'])
def create_farm_form():
	return render_template('forms/new_farm.html', form=FarmForm())

@app.route('/products/create', methods=['GET'])
def create_product_form():
	return render_template('forms/new_product.html', form=ProductForm())
