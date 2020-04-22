from flask import Flask, jsonify, render_template
from flask import current_app as app

@app.route('/')
def hello():
	user = {'username': 'Miguel'}
	# return jsonify({'message': 'HELLO WOLRD'})
	return render_template('index.html', title='Home', user=user)