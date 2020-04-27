#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Imports
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
import os
basedir = os.path.abspath(os.path.dirname(__file__))


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Configuration Settings
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
class Config(object):

### TODO Switch to local redirect for local run ###
#--------------------------------------------------------------------------------------------#
	# AUTH0_REDIRECT = 'http://127.0.0.1:5000/'
	AUTH0_REDIRECT = 'https://fsdn-farm-shop.herokuapp.com/'

# Product tests
# -------------------------------------------------------------------------------------------#
	DEBUG = True
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'this-is-my-secret-key'
	AUTH0_DOMAIN = 'fsnd-victorcocuz.auth0.com'
	AUTH0_AUDIENCE = 'farm_shop_api'
	AUTH0_RESPONSE_TYPE = 'token'
	AUTH0_CLIENT_ID = 'NCvcf0H0XLMpzg5xWGh3jJGcqve0or5c'
	REQUEST_URI = "https://{}/authorize?audience={}&response_type={}&client_id={}&redirect_uri={}".format(AUTH0_DOMAIN, AUTH0_AUDIENCE, AUTH0_RESPONSE_TYPE, AUTH0_CLIENT_ID, AUTH0_REDIRECT)

	JWT_SECRET_KEY = 'this-is-my-jwt-secret-key'
	JWT_TOKEN_LOCATION = 'cookies'
	JWT_ACCESS_COOKIE_PATH = '/'
	JWT_REFRESH_COOKIE_PATH = '/token'
	JWT_COOKIE_CSRF_PROTECT = True
	JWT_CSRF_CHECK_FORM = True
	JWT_ALGORITHM = 'RS256'


class ProductionConfig(Config):
	DEBUG = False
	AUTH0_REDIRECT = 'https://fsdn-farm-shop.herokuapp.com/'

class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
	DEBUG = False
	AUTH0_REDIRECT = 'http://127.0.0.1:5000/'