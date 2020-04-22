from flask import Flask, jsonify
import logging

def create_app(test_config=None):
	app = Flask(__name__)

	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)

	@app.route('/')
	def hello():
		return jsonify({'message': 'HELLO WOLRD'})

	return app