from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, AnyOf, Regexp, Optional
from app.models import PaymentInfo, OrderInfo
from flask_wtf.file import FileRequired

class PaymentForm(FlaskForm):
	name = StringField('First Name', validators=[DataRequired()])
	cardtype = SelectField(u'Card Type', choices = [('c',"Credit"), ('d',"Debit")],validators = [Optional()])
	cardnumber = StringField('Card Number',validators=[DataRequired()])
	card_exp = StringField('Expiration Date', validators=[Regexp("\d{2}/\d{4}")])
	address = StringField('Address', validators=[DataRequired()])
	card_cvv=IntegerField('CVV', validators=[DataRequired()])
	city = StringField('City', validators=[DataRequired()])
	state = StringField('State', validators=[DataRequired()])
	zip_code = StringField('Zip', validators=[DataRequired()])
	tip = DecimalField('Tip', validators=[Optional()])
	submit = SubmitField('Place Payment')

	def validate_card_num(self, card_num):
		if not len(str(card_num.data))==16:
			raise ValidationError('Credit card number should be 16 digits long')

class LoginForm(FlaskForm):
    employee_id = StringField('Employee Id', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_employee_id(self, employee_id):
        if not len(str(employee_id.data))==8:
            raise ValidationError('Credit card number should be 8 digits long')

class OrderEntryForm(FlaskForm):
	employee_id = IntegerField('Employee Id', validators=[DataRequired()])
	item = StringField('Menu Item', validators=[DataRequired()])
	price = DecimalField('Price', validators=[DataRequired()])
	table = IntegerField('Table Number', validators=[DataRequired()])
	submit = SubmitField('Add Order')

class TableToCharge(FlaskForm):
	table = IntegerField('Table Number', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(),Email()])
	submit = SubmitField('Send Bill')

