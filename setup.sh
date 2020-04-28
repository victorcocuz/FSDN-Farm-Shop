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