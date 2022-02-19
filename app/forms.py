from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, AnyOf, Regexp, Optional
#from app.models import User, Book, Promotion, Order, ListItem
from flask_wtf.file import FileRequired

class PaymentForm(FlaskForm):
	name = StringField('First Name', validators=[DataRequired()])
	cardtype = StringField('Card Type', validators = [Optional()])
	cardnumber = StringField('Card Number', validators=[DataRequired()])
	card_exp = StringField('Expiration Date', validators=[Regexp("\d{2}/\d{4}")])
	address = StringField('Address', validators=[DataRequired()])
	city = StringField('City', validators=[DataRequired()])
	state = StringField('State', validators=[DataRequired()])
	zip_code = StringField('Zip', validators=[DataRequired()])

	def validate_card_num(self, card_num):
		if not len(str(card_num.data))==16:
			raise ValidationError('Credit card number should be 16 digits long')

#choices = [('c',"Credit"), ('d',"Debit")]