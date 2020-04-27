
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Imports
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
import os
import unittest
import json
import logging
from flask_sqlalchemy import SQLAlchemy

from application import flask_app
from application.models import db, setup_db, Farm, Product
from auth import AuthError


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Tests
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# A class representing the Farm Shop test case
# -------------------------------------------------------------------------------------------#
class FarmShopTestCase(unittest.TestCase):

	def setUp(self):
		self.app = flask_app
		self.client = self.app.test_client
		setup_db(self.app)

		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			self.db.create_all()

		self.administrator_bearer = ('Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtjWW5OZGEyY3FlQndJSUhHa21IUyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdmljdG9yY29jdXouYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEyMTIxNjk1Mzc5NzMwODg2NDc0IiwiYXVkIjpbImZhcm1fc2hvcF9hcGkiLCJodHRwczovL2ZzbmQtdmljdG9yY29jdXouYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4ODAwNTE0MSwiZXhwIjoxNTg4MDkxNTQxLCJhenAiOiJOQ3ZjZjBIMFhMTXB6ZzV4V0doM2pKR2NxdmUwb3I1YyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJlZGl0OmZhcm0iLCJlZGl0OnByb2R1Y3QiXX0.hYxc8YZorxQ3ZuSteeBYx2VgEbqr8NUROlKJjqysOKVIGoQNJx8FTrgJ7PuiVg_TWt1Gi5vvvcuZCjIcWE0uqD5bB3kwfYRVgC73OpDT38BuxK6hsGLPeJiRffd4Hp0V6n3tWSwDrHX3DwNDRzFQk3jClO6LlUzZZEfIjBF9mY6dMFP9okOTcBg-XXahO_ecRNeLktDLbJ5nMIIogxWHWFernkaHGfqI-xJjY9jpEnXDcRU96-rIeltDi9hfhSnIHUgwnwHaSvo2ihRVbIgJQ0x7CotUzPSpPTK4IyFX43uJO7-JtbSxZepsRw-q1JKFaMj5Z6N26FQ2raoBTo7yFw')
		self.employee_bearer = ('Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtjWW5OZGEyY3FlQndJSUhHa21IUyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdmljdG9yY29jdXouYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAxNjA5NjgyNTgwNDQ0NDAxNDMzIiwiYXVkIjpbImZhcm1fc2hvcF9hcGkiLCJodHRwczovL2ZzbmQtdmljdG9yY29jdXouYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4ODAwNTIwMiwiZXhwIjoxNTg4MDkxNjAyLCJhenAiOiJOQ3ZjZjBIMFhMTXB6ZzV4V0doM2pKR2NxdmUwb3I1YyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJlZGl0OnByb2R1Y3QiXX0.AO6dbdDFll8ciZ79lziw_2xz7dLcyXpgQPIb7hs8Dyi8mrOwQtTJCa1O3hAAarj9EXJCz_vHgEA59HKGiBPcNOYo3OvyRNL1ejynqFtg6zPIymBS6G7_EqJbsAn2tEVXhaVer2lZeE6wyPcA3SRNcKXrxJtBjfoXyGGY6PJZaq7SbqIB0vzqFlBDeAJ6DwY010Ji51HTxvQMpelAyxO-sMiJ-gDop09bG44m2uDaHriE4ovBZMdAax1ORhRvKsLVY5S68vWG2jsXP06y2rVdyDJqQAqoFdqCbO7UqSZnqifoqXkt8Av5j3A_tFr8MyK3ww8LCrFZrJ_vbumYA3HisA')

		self.test_farm = {
		'name': 'Test Farm Name',
		'address': 'Test Address',
		'city': 'Test City'
		}

		self.test_farm_update = {
		'name': 'Test Farm Name 2',
		'address': 'Test Address 2',
		'city': 'Test City 2'
		}

		self.test_product = {
		'name': 'Test Product Name',
		'quantity': 1
		}

		self.test_product_update = {
		'name': 'Test Product Name 2',
		'quantity': 2
		}
	
	def tearDown(self):
		pass

	def create_farm(self):
		res = self.client().post(
			'/farms/0/new',
			data=dict(name=self.test_farm['name'], address=self.test_farm['address'], city=self.test_farm['city']),
			headers={'Authorization': self.administrator_bearer}
			)
		return res

	def create_product(self, farm_id):
		res = self.client().post(
			'/farms/' + str(farm_id) + '/products/0/new',
			data=dict(name=self.test_product['name'], quantity=self.test_product['quantity']),
			headers={'Authorization': self.administrator_bearer}
			)
		return res

	def delete_farm_and_product(self):
		db.session.query(Product).filter(Product.name==self.test_product['name']).delete()
		db.session.query(Product).filter(Product.name==self.test_product_update['name']).delete()
		db.session.query(Farm).filter(Farm.name==self.test_farm['name']).delete()
		db.session.query(Farm).filter(Farm.name==self.test_farm_update['name']).delete()
		db.session.commit()
		return ({'success': True})


# General tests
# -------------------------------------------------------------------------------------------#
	# Success test the '/' endpoint with GET method to load the main page
	def test_index(self):
		res = self.client().get('/')
		self.assertEqual(res.status_code, 302)

	# Fail test the '/' endpoint with GET method to load the main page with a wrong url
	def test_index_wrong_url(self):
		res = self.client().get('/a')
		self.assertEqual(res.status_code, 404)

	# Success test the '/login' endpoint with GET method to load the login page
	def test_login(self):
		res = self.client().get('/login')
		self.assertEqual(res.status_code, 200)

	# Fail test the '/login' endpoint with GET method to load the login page with a wrong url
	def test_login_wrong_url(self):
		res = self.client().get('/logins')
		self.assertEqual(res.status_code, 404)

# Farm tests
# -------------------------------------------------------------------------------------------#
	# Success test the '/farms' endpoint with GET method to load the farms page
	def test_get_farms(self):
		res = self.client().get('/farms')
		self.assertEqual(res.status_code, 200)

	# Fail test the '/farms' endpoint with GET method to load the farms page with a wrong url
	def test_get_farms_wrong_url(self):
		res = self.client().get('/farmers')
		self.assertEqual(res.status_code, 404)

	# Success test the '/farms/0/new' endpoint with GET method to load a new farm form
	def test_get_farms_form_create(self):
		res = self.client().get(
			'/farms/0/new',
			headers={'Authorization': self.administrator_bearer}
			)
		self.assertEqual(res.status_code, 200)

	# Fail test the '/farms/0/new' endpoint with GET method to load a new farm form with wrong token
	def test_get_farms_form_create_wrong_token(self):
		res = self.client().get(
			'/farms/0/new',
			headers={'Authorization': 'Bearer token'}
			)
		self.assertEqual(res.status_code, 401)

	# Success test the '/farms/<int:farm_id>/update' endpoint with GET method to load an existing farm form
	def test_get_farms_form_update(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id

		res = self.client().get(
			'/farms/{}/update'.format(str(farm_id)),
			headers={'Authorization': self.administrator_bearer}
			)	

		self.assertEqual(res.status_code, 200)	
		self.delete_farm_and_product()

	# Fail test the '/farms/<int:farm_id>/update' endpoint with GET method to load an existing farm form with wrong token
	def test_get_farms_form_update_wrong_token(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id

		res = self.client().get(
			'/farms/{}/update'.format(str(farm_id)),
			headers={'Authorization': 'Bearer token'}
			)	

		self.assertEqual(res.status_code, 401)	
		self.delete_farm_and_product()

	# Success test the '/farms/0/new' endpoint with POST method to create a new farm
	def test_post_create_farm(self):
		total_farms_before = len(Farm.query.all())
		res = self.create_farm()
		total_farms_after = len(Farm.query.all())

		self.assertEqual(res.status_code, 302)
		self.assertEqual(total_farms_before, total_farms_after - 1)
		self.delete_farm_and_product()

	# Fail test the '/farms/0/new' endpoint with POST method to create a new farm with wrong token
	def test_post_farms_form_create_wrong_token(self):
		res = self.client().post(
			'/farms/0/new',
			data=dict(name=self.test_farm['name'], address=self.test_farm['address'], city=self.test_farm['city']),
			headers={'Authorization': 'Bearer token'}
			)
		self.assertEqual(res.status_code, 401)

	# Success test the '/farms/<int:farm_id>/update' endpoint with POST or PATCH method to update an existing farm
	def test_post_farms_update(self):
		self.create_farm()
		farm = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first()
		farm_id = farm.id

		res = self.client().patch(
			'/farms/{}/update'.format(str(farm_id)),
			data=dict(name=self.test_farm_update['name'], address=self.test_farm_update['address'], city=self.test_farm_update['city']),
			headers={'Authorization': self.administrator_bearer}
			)

		farm = db.session.query(Farm).filter(Farm.name==self.test_farm_update['name']).first()

		self.assertEqual(res.status_code, 302)
		self.assertEqual(farm.name, self.test_farm_update['name'])
		self.assertEqual(farm.address, self.test_farm_update['address'])
		self.assertEqual(farm.city, self.test_farm_update['city'])
		self.delete_farm_and_product()

	# Fail test the '/farms/<int:farm_id>/update' endpoint with POST or PATCH method to update an existing farm with wrong token
	def test_post_farms_update_wrong_token(self):
		self.create_farm()
		farm = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first()
		farm_id = farm.id

		farm.name = self.test_farm_update['name']
		farm.address = self.test_farm_update['address']
		farm.city = self.test_farm_update['city']

		db.session.commit()

		res = self.client().patch(
			'/farms/{}/update'.format(str(farm_id)),
			headers={'Authorization': 'Bearer token'}
			)

		farm = db.session.query(Farm).filter(Farm.name==self.test_farm_update['name']).first()

		self.assertEqual(res.status_code, 401)
		self.delete_farm_and_product()

	# Success test the '/farms/<int:farm_id>' endpoint with DELETE method to delete a farm
	def test_delete_farm(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id

		res = self.client().delete('/farms/{}'.format(farm_id),
			headers={'Authorization': self.administrator_bearer}
			)
		self.assertEqual(res.status_code, 200)

	# Fail test the '/farms/<int:farm_id>' endpoint with DELETE method to delete a farm with a wrong url
	def test_delete_farm_wrong_url(self):
		res = self.client().delete('/farms/a',
			headers={'Authorization': self.administrator_bearer}
			)
		self.assertEqual(res.status_code, 404)

# Product tests
# -------------------------------------------------------------------------------------------#
	# Success test the '/farms/<int:farm_id>/products' endpoint with GET method to load the products page
	def test_get_products(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id

		res = self.client().get('/farms/{}/products'.format(str(farm_id)))
		self.assertEqual(res.status_code, 200)
		self.delete_farm_and_product()

	# Fail test the '/farms/<int:farm_id>/products' endpoint with GET method to load the products page with wrong url
	def test_get_products_wrong_url(self):
		res = self.client().get('/farms/a')
		self.assertEqual(res.status_code, 404)

	# Success test the '/farms/<int:farm_id>/products/0/new' endpoint with GET method to load a new product form
	def test_get_products_form_create(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id		
		
		res = self.client().get(
			'/farms/{}/products/0/new'.format(str(farm_id)),
			headers={'Authorization': self.administrator_bearer}
			)
		self.assertEqual(res.status_code, 200)
		self.delete_farm_and_product()

	# Fail test the '/farms/<int:farm_id>/products/0/new' endpoint with GET method to load a new product form with wrong token
	def test_get_products_form_create_wrong_token(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id		
		
		res = self.client().get(
			'/farms/{}/products/0/new'.format(str(farm_id)),
			headers={'Authorization': 'Bearer token'}
			)
		self.assertEqual(res.status_code, 401)
		self.delete_farm_and_product()

	# Success test the '/farms/<int:farm_id>/products<int:product_id>' endpoint with GET method to load an existing product form
	def test_get_products_form_update(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id
		res = self.create_product(farm_id)
		product_id = db.session.query(Product).filter(Product.name==self.test_product['name']).first().id

		res = self.client().get(
			'/farms/{}/products/{}'.format(str(farm_id), str(product_id)),
			headers={'Authorization': self.administrator_bearer}
			)		

		self.assertEqual(res.status_code, 200)	
		self.delete_farm_and_product()

	# Fail test the '/farms/<int:farm_id>/products<int:product_id>' endpoint with GET method to load an existing product form with wrong token
	def test_get_products_form_update_wrong_token(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id
		res = self.create_product(farm_id)
		product_id = db.session.query(Product).filter(Product.name==self.test_product['name']).first().id
		
		res = self.client().get(
			'/farms/{}/products/{}'.format(str(farm_id), str(product_id)),
			headers={'Authorization': 'Bearer token'}
			)		

		self.assertEqual(res.status_code, 401)	
		self.delete_farm_and_product()

	# Success test the '/farms/<int:farm_id>/products/0/new' endpoint with POST method to create a new product
	def test_post_products_form_create(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id		

		total_products_before = len(db.session.query(Product).filter(Product.farm_id==farm_id).all())
		res = self.create_product(farm_id)
		total_products_after = len(db.session.query(Product).filter(Product.farm_id==farm_id).all())

		self.assertEqual(res.status_code, 302)
		self.assertEqual(total_products_before, total_products_after - 1)
		self.delete_farm_and_product()


	# Fail test the '/farms/<int:farm_id>/products/0/new' endpoint with POST method to create a new product with wrong token
	def test_post_products_form_create_wrong_token(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id		

		res = self.client().post(
			'/farms/{}/products/0/new'.format(str(farm_id)),
			data=dict(name=self.test_product['name'], quantity=self.test_product['quantity']),
			headers={'Authorization': 'Bearer token'}
			)

		self.assertEqual(res.status_code, 401)
		self.delete_farm_and_product()

	# Success test the '/farms/<int:farm_id>/products/<int:product_id>' endpoint with POST or PATCH method to update an existing product
	def test_post_products_form_update(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id
		self.create_product(farm_id)
		product_id = db.session.query(Product).filter(Product.farm_id==farm_id).filter(Product.name==self.test_product['name']).first().id
		
		res = self.client().patch(
			'/farms/{}/products/{}'.format(str(farm_id), str(product_id)),
			data=dict(name=self.test_product_update['name'], quantity=self.test_product_update['quantity']),
			headers={'Authorization': self.employee_bearer}
			)		

		product = db.session.query(Product).filter(Product.id==product_id).first()

		self.assertEqual(res.status_code, 302)
		self.assertEqual(product.name, self.test_product_update['name'])
		self.assertEqual(product.quantity, self.test_product_update['quantity'])
		self.delete_farm_and_product()

	# Fail test the '/farms/<int:farm_id>/products/<int:product_id>' endpoint with POST or PATCH method to update an existing product with wrong token
	def test_post_products_form_update_wrong_token(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id
		self.create_product(farm_id)
		product_id = db.session.query(Product).filter(Product.farm_id==farm_id).filter(Product.name==self.test_product['name']).first().id

		res = self.client().patch(
			'/farms/{}/products/{}'.format(str(farm_id), str(1000)),
			data=dict(name=self.test_product_update['name'], quantity=self.test_product_update['quantity']),
			headers={'Authorization': 'Bearer token'}
			)		

		self.assertEqual(res.status_code, 401)

	# Success test the '/farms/<int:farm_id>/products/<int:product_id>' endpoint with DELETE method to delete a product
	def test_delete_product(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id
		self.create_product(farm_id)
		product_id = db.session.query(Product).filter(Product.name==self.test_product['name']).first().id

		res = self.client().delete('/farms/{}/products/{}'.format(farm_id, product_id),
			headers={'Authorization': self.employee_bearer}
			)
		self.assertEqual(res.status_code, 200)

	# Fail test the '/farms/<int:farm_id>/products/<int:product_id>' endpoint with DELETE method to delete a product with wrong bearer
	def test_delete_product_wrong_token(self):
		self.create_farm()
		farm_id = db.session.query(Farm).filter(Farm.name==self.test_farm['name']).first().id
		self.create_product(farm_id)
		product_id = db.session.query(Product).filter(Product.name==self.test_product['name']).first().id

		res = self.client().delete('/farms/{}/products/{}'.format(farm_id, product_id),
			headers={'Authorization': 'Bearer token'}
			)
		self.assertEqual(res.status_code, 401)
		self.delete_farm_and_product()

# Execute tests
# -------------------------------------------------------------------------------------------#
if __name__ == "__main__":
	unittest.main()