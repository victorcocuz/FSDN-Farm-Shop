from flask import Flask, jsonify
from flask import current_app as app

@app.route('/')
def hello():
	return jsonify({'message': 'HELLO WOLRD'})