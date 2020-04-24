from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_database_path(app):
	# database_name = app.config.get('DATABASE_NAME')
	# database_user = app.config.get('DATABASE_USER')
	# database_password = app.config.get('DATABASE_PASSWORD')
	# database_host = app.config.get('DATABASE_HOST')
	# return "postgres://{}:{}@{}/{}".format(database_user, database_password, database_host, database_name)
	return "postgresql:///fsdn-farm-shop"

def setup_db(app):
	app.config["SQLALCHEMY_DATABASE_URI"] = get_database_path(app)
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	db.init_app(app)
	db.create_all()

class Farm(db.Model):
	__tablename__ = 'farm'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120))
	address = db.Column(db.String(120))
	city = db.Column(db.String(32))

	product = db.relationship('Product', backref='farm', lazy=True)


class Product(db.Model):
	__tablename__ = 'product'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120))
	quantity = db.Column(db.Integer)
	
	farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))