# FSDN Farm Shop
**Version 1.0.0**

## Description and motivation
### Intro
Farm Shop is the capstone project for the Udacity Full Stack Developer Nanodegree. It has been created to apply all the skills acquired during the course. 

### Topic
The topic of choice is a farm shop application that connects farmers and potential customers. Farmers are able to list their own farms and products. Customers can view all listings.

### Permissions
There are three levels of access to the application:
- Customers - Can view all farms and all products
- Farm Employees - Have all the customers permissions + Can CREATE / UPDATE / DELETE any product within their farms
- Administrator - Has all the Employee permissions + Can CREATE / UPDATE / DELETE any farm


## Requirements
Models will include at least…
	Two classes with primary keys at at least two attributes each
	[Optional but encouraged] One-to-many or many-to-many relationships between classes
Endpoints will include at least…
	Two GET requests
	One POST request
	One PATCH request
	One DELETE request
Roles will include at least…
	Two roles with different permissions
	Permissions specified for all endpoints
Tests will include at least…
	One test for success behavior of each endpoint
	One test for error behavior of each endpoint
	At least two tests of RBAC for each role


## Installation Instructions
### Heroku Server
The project has been uploaded on Heroku. The URL to access it is:
https://fsdn-farm-shop.herokuapp.com/

### Local Installation
The full functionality is implemented on the Heroku server. However, for reviewing the code and the tests, please follow the instructions below:

1. Fork and clone the repository.
2. Create a virtual environment.
3. Install all dependencies by running `pip install requirements.txt`.
4. Run the following commands in the project folder to run the application:
```
export FLASK_APP=run.py
export DATABASE_URL='postgres://victor:victor16@localhost:5432/fsdn_farm_shop'
flask run
```

**Note: The app configuration can be changed from the `__init__.py` file, by changing the following line:**
```
	config_name = os.getenv('FLASK_CONFIGURATION', 'production')
```

You can choose any of the options below:
```
config = {
	"production": ProductionConfig,
	"staging": StagingConfig,
	"development": DevelopmentConfig,
	"testing": TestingConfig,
	"default": DevelopmentConfig
}
```

**NOTE: There have been some issues with configurations, so if this doesn't work, open `config.py` and comment out the heroku redirect and uncomment the local redirect, as per below:**
```
AUTH0_REDIRECT = 'http://127.0.0.1:5000/'
# AUTH0_REDIRECT = 'https://fsdn-farm-shop.herokuapp.com/'
```

### Testing
Te test file contains 28 tests, two for each endpoint provided (one for success and one for fail). Some of these do not require a token, some have been tested against the employee role and some against the administrator role.

To successfully run the tests, debug must be set to false: `export DEBUG=False`

Testing can be done by changing the directory to the project folder and running `py test_application.py` *on Windows 10*.

**NOTE: The bearer tokens provided in the tests do expire. These can be replaced with tokens copied from the url upon successful login.**


## Use Instructions

### Login
To fully access and test the app a login will be required. Without login information, the user will only have access to view the farms and the products, but will not be able to edit anything.

**NOTE: Login instructions will be provided in a separate note or upon request.**

**Logging in**
1. To login simply follow the login link and then press on the login link below. 
2. Choose gmail login and insert the user and password provided.
3. Once successful, copy the url and retain the token for testing.
4. You should now have access as per the roles described above.

### Farms
Viewing farms does not require authentication. Click on `home` to view farms.

Editing farms requires administrator permissions. Once authentication is successful, the user can add, update and remove farms.

Deleting a farm will delete all associated products.

**NOTE: To update a farm the user will need to refill all the fields.**

### Products
Viewing products does not require authentication. Click on the name of any farm to view products belonging to that farm.

Editing products requires either administrator or employee permissions. Once authentication is successful, the user can add, update and remove products.

**NOTE: The product quantity field can only take a number. There are no validators for it at the moment.**


## Frontend
This was not required, but has been created to get an understanding of how a full website should function. It is incomplete and has no style added. At this point, its only purpose is to serve the endpoints.


## Backend - Endpoints
This has been created as per requirements above. 

### Summary
GET '/'
GET '/login'
GET '/farms'
GET '/farms/0/new'
GET '/farms/<int:farm_id>/update'
POST '/farms/0/new'
PATCH '/farms/<int:farm_id>/update'
DELETE '/farms/<int:farm_id>'
GET '/farms/<int:farm_id>/products'
GET '/farms/<int:farm_id>/products/0/new'
GET '/farms/<int:farm_id>/products/<int:product_id>'
POST '/farms/<int:farm_id>/products/0/new'
PATCH '/farms/<int:farm_id>/products/<int:product_id>'
DELETE '/farms/<int:farm_id>/products/<int:product_id>'

### GET '/'
- Description: Redirects to '/farms' URL
- Request arguments: None
- Returns: A redirect to the '/farms' endpoint

### GET '/login'
- Description: Loads the login page
- Request arguments: None
- Returns: Renders a html template and sends a login_uri, compiled from app.config

### GET '/farms'
- Description: Loads a page that displays all farms
- Request Arguments: None
- Returns: Renders a html template and sends the farm data fetched from the database

### GET '/farms/0/new'
- Description: Loads a new farms form
- Request Arguments: None
- Requires Auth and permission 'edit:farm'
- Returns: Renders a html template and sends a WTF Form

### GET '/farms/<int:farm_id>/update'
- Description: Loads a form for an existing farm
- Request Arguments: farm_id
- Requires Auth and permission 'edit:farm'
- Returns: Renders a html template, sends a WTF Form and the farm data to update based on the farm_id

### POST '/farms/0/new'
- Description: Adds a new farm to the database
- Request Arguments: None
- Requires Auth and permission 'edit:farm'
- Returns: A redirect to the '/farms' endpoint

### PATCH '/farms/<int:farm_id>/update'
- Description: Updates an existing farm from the databse
- Request Arguments: farm_id
- Requires Auth and permission 'edit:farm'
- Returns: A redirect to the '/farms' endpoint

### DELETE '/farms/<int:farm_id>'
- Description: Deletes a farm from the database
- Request Arguments: farm_id
- Requires Auth and permission 'edit:farm'
- Returns: A json confirming the success of the operation

### GET '/farms/<int:farm_id>/products'
- Description: Loads a page that displays all products
- Request Arguments: farm_id
- Returns: A html template and sends the products data fetched from the database which belongs to the farm of id farm_id

### GET '/farms/<int:farm_id>/products/0/new'
- Description: Loads a new products form
- Request Arguments: farm_id
- Requires Auth and permission 'edit:product'
- Returns: A html template, sends a WTF form and the farm_id for the user to add a new product

### GET '/farms/<int:farm_id>/products/<int:product_id>'
- Description: Loads a form for an existing product
- Request Arguments: farm_id, product_id
- Requires Auth and permission 'edit:product'
- Returns: A html template, sends a WTF form, the farm_id and the current product_id for the user to update

### POST '/farms/<int:farm_id>/products/0/new'
- Description: Adds a new product to the database
- Request Arguments: farm_id
- Requires Auth and permission 'edit:product'
- Returns: A redirect to '/farms/<int:farm_id>/products' endpoint and sends the current farm_id

### PATCH '/farms/<int:farm_id>/products/<int:product_id>'
- Description: Updates an existing product from the database
- Request Arguments: farm_id, product_id
- Requires Auth and permission 'edit:product'
- Returns: A redirect to '/farms/<int:farm_id>/products' endpoint and sends the current farm_id

### DELETE '/farms/<int:farm_id>/products/<int:product_id>'
- Description: Deletes a product from the database
- Request Arguments: farm_id, product_id
- Requires Auth and permission 'edit:product'
- Returns: A json confirming the success of the operation