from flask import Flask, jsonify
import logging

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)

	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)

	with app.app_context():
		from application import views

	return app

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=8080, debug=True)