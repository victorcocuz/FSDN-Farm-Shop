import logging
from flask import Flask, jsonify
from config import DevelopmentConfig

# from .. import config

def create_app(test_config=None):
	app = Flask(__name__)
	app.config.from_object(DevelopmentConfig)

	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)

	with app.app_context():
		from application import routes

	return app

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=8080, debug=True)