#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Imports
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask import current_app as app
from application.forms import LoginForm, FarmForm, ProductForm
from application.models import Farm, Product, db
from sqlalchemy.exc import SQLAlchemyError

import logging


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# General
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Index
# -----------------------------------------------------------------------#
@app.route('/')
def index():
	return redirect(url_for('farms'))

# Login
# -----------------------------------------------------------------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
			form.username.data, form.remember_me.data))
		return redirect(url_for('farms'))
	return render_template('pages/login.html', title='sign In', form=form)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Farms
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Show all farms
# -----------------------------------------------------------------------#
@app.route('/farms', methods=['GET'])
def farms():
	farms = db.session.query(Farm).order_by(Farm.name).all()
	data = []
	for farm in farms:
		data.append({
			'id': farm.id,
			'name': farm.name,
			'address': farm.address,
			'city': farm.city
			})
	return render_template('pages/farms.html', title='Farms', data=data)

# Load a new farm form or an update existing farm form
# -----------------------------------------------------------------------#
@app.route('/farms/farm', methods=['GET'])
def create_farm_form():
	return render_template('forms/new_farm.html', form=FarmForm())

@app.route('/farms/<int:farm_id>/update', methods=['GET'])
def update_farm_form(farm_id):
	farm = db.session.query(Farm).filter(Farm.id==farm_id).scalar()
	return render_template('forms/new_farm.html', form=FarmForm(), farm=farm)

# Add a new farm
# -----------------------------------------------------------------------#
@app.route('/farms/farm', methods=['POST'])
def create_farm_submission():
	try:
		farm = Farm(
			name=request.form.get('name'),
			address=request.form.get('address'),
			city=request.form.get('city')
			)

		db.session.add(farm)
		db.session.commit()
		flash('Farm ' + request.form.get('name') + ' was successfully listed!')
	except SQLAlchemyError as e:
		flash('An error occured. Farm ' + request.form.get('name') + ' could not be listed!')	
		db.session.rollback()
		return e
	finally:
		db.session.close()
	return redirect(url_for('farms'))

# Update an existing farm
# -----------------------------------------------------------------------#
@app.route('/farms/<int:farm_id>/update', methods=['POST'])
def update_farm(farm_id):
	try:
		farm = db.session.query(Farm).filter(Farm.id==farm_id).scalar()
		farm.name = request.form.get('name')
		farm.address = request.form.get('address')
		farm.city = request.form.get('address')

		db.session.commit()
	except SQLAlchemyError as e:
		db.session.rollback()
		return e
	finally:
		db.session.close()
	return redirect(url_for('farms'))
	
# Delete a farm
# -----------------------------------------------------------------------#
@app.route('/farms/<int:farm_id>', methods=['DELETE'])
def delete_farm(farm_id):
	logging.error('fuuuuuck')
	logging.error(farm_id)
	try:
		db.session.query(Farm).filter(Farm.id==farm_id).delete()
		db.session.commit()
	except SQLAlchemyError as e:
		db.session.rollback()
		return e
	finally:
		db.session.close()
	return jsonify({ 'success': True })


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Products
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Show all products for a specific farm
# -----------------------------------------------------------------------#
@app.route('/farms/<int:farm_id>', methods=['GET'])
def show_products(farm_id):
	products = db.session.query(Product).join(Farm, Farm.id==Product.farm_id).filter(Farm.id==farm_id).order_by(Product.name).all()
	
	response = []
	data = []
	
	for product in products:
		response.append({
			'id': product.id,
			'name': product.name,
			'quantity': product.quantity
			})

	data = {
	'farm': db.session.query(Farm).filter(Farm.id==farm_id).scalar(),
	'products': response
	}
	return render_template('pages/products.html', data=data)

# Load a new product form or an update an existin product form
# -----------------------------------------------------------------------#
@app.route('/farms/<int:farm_id>/product', methods=['GET'])
def create_product_form(farm_id):
	return render_template('forms/new_product.html', form=ProductForm(), farm_id=farm_id)

@app.route('/farms/<int:farm_id>/<int:product_id>', methods=['GET'])
def update_product_form(farm_id, product_id):
	product = db.session.query(Product).filter(Product.id==product_id).scalar()
	return render_template('forms/new_product.html', form=ProductForm(), farm_id=farm_id, product=product)


# Add a new product
# -----------------------------------------------------------------------#
@app.route('/farms/<int:farm_id>/product', methods=['POST'])
def create_product_submission(farm_id):
	try:
		product = Product(
			name=request.form.get('name'),
			quantity=request.form.get('quantity'),
			farm_id=farm_id
			)

		db.session.add(product)
		db.session.commit()
		flash('Product ' + request.form.get('name') + ' was successfully listed!')
	except SQLAlchemyError as e:
		flash('An error occured. Product ' + request.form.get('name') + ' could not be listed!')	
		db.session.rollback()
		return e
	finally:
		db.session.close()
	return redirect(url_for('show_products', farm_id=farm_id))

# Update an existing product
# -----------------------------------------------------------------------#
@app.route('/farms/<int:farm_id>/<int:product_id>', methods=['POST'])
def update_product(farm_id, product_id):
	try:
		product = db.session.query(Product).filter(Product.farm_id==farm_id).filter(Product.id==product_id).scalar()
		product.name = request.form.get('name')
		product.quantity = request.form.get('quantity')

		db.session.commit()
	except SQLAlchemyError as e:
		db.session.rollback()
		return e
	finally:
		db.session.close()
	return redirect(url_for('show_products', farm_id=farm_id))

# Delete a product
# -----------------------------------------------------------------------#
@app.route('/<int:farm_id>/products/<int:product_id>', methods=['DELETE'])
def delete_product(farm_id, product_id):
	try:
		db.session.query(Product).filter(Product.farm_id==farm_id).filter(Product.id==product_id).delete()
		db.session.commit()
	except SQLAlchemyError as e:
		db.session.rollback()
		return e
	finally:
		db.session.close()
	return jsonify({ 'success': True })
