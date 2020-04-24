import os
import logging
from flask import Flask, jsonify
from config import ProductionConfig, StagingConfig, DevelopmentConfig, TestingConfig
from flask_migrate import Migrate
from flask_cors import CORS

config = {
	"production": ProductionConfig,
	"staging": StagingConfig,
	"development": DevelopmentConfig,
	"testing": TestingConfig,
	"default": DevelopmentConfig
}

def configure_app(app):
	config_name = os.getenv('FLASK_CONFIGURATION', 'default')
	app.config.from_object(config[config_name])
	app.config.from_pyfile('config.cfg', silent=True)

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	configure_app(app)

	with app.app_context():
		from application import routes
		from application.models import setup_db, db

	setup_db(app)
	migrate = Migrate(app, db)
	cors = CORS(app, resources={r"/*": {"origins": "*"}})

	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
		response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
		return response
	
	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)
	
	logging.info(os.environ.get('DATABASE_URL'))

	return app

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=8080, debug=True)