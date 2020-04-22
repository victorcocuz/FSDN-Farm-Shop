from flask import Flask, jsonify
import logging

# def create_app(test_config=None):
app = Flask(__name__, instance_relative_config=True)

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

@app.route('/')
def hello():
	return jsonify({'message': 'HELLO WOLRD'})

# 	return app

# APP = create_app()

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)