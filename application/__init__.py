from flask import Flask, jsonify
import logging

def create_app(test_config=None):
	app = Flask(__name__)

	@app.route('/')
	def hello():
		print ("whatever")
		logging.error('come on')
		return jsonify({'message': 'HELLO WOLRD'})

	return app