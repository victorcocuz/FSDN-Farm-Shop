# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Imports and global variables
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Models and methods
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Method to set up the database path for local use
# -------------------------------------------------------------------------------------------#
def get_database_path(app):
    database_name = app.config.get('DATABASE_NAME')
    database_user = app.config.get('DATABASE_USER')
    database_password = app.config.get('DATABASE_PASSWORD')
    database_host = app.config.get('DATABASE_HOST')
    return "postgres://{}:{}@{}/{}".format(
        database_user,
        database_password,
        database_host,
        database_name
    )

# Method to set up the app database. This will be called from __init__.py
# -------------------------------------------------------------------------------------------#


def setup_db(app):
    # app.config["SQLALCHEMY_DATABASE_URI"] = get_database_path(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

# Farm model to include all farm information in the database
# -------------------------------------------------------------------------------------------#


class Farm(db.Model):
    __tablename__ = 'farm'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(32))

    product = db.relationship('Product', backref='farm', lazy=True)

# Product model to include all roduct information in the database.
# -------------------------------------------------------------------------------------------#


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    quantity = db.Column(db.Integer)

    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))
