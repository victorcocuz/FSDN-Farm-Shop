from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class FarmForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	address = StringField('address', validators=[DataRequired()])
	city = StringField('city', validators=[DataRequired()])

class ProductForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	quantity = IntegerField('quantity', validators=[DataRequired()])