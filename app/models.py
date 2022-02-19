from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class PaymentInfo(db.Model):
	orderNumber = db.Column(db.Integer, primary_key=True, unique=True, index=True)
	card_num = db.Column(db.String(128), nullable=True)
	card_exp = db.Column(db.String(128), nullable=True)
	cardtype = db.Column(db.String(1), nullable=True)
	name = db.Column(db.String(128), nullable=True)
	address = db.Column(db.String(128), nullable=True)
	city = db.Column(db.String(128), nullable=True)
	state = db.Column(db.String(128), nullable=True) 
	zip_code = db.Column(db.String(128), nullable=True)
	employee_id = db.Column(db.Integer, nullable= True)

	def set_card_num(self, card_num):
		self.card_num = generate_password_hash(str(card_num))
	def set_card_exp(self, card_exp):
		self.card_exp = generate_password_hash(str(card_exp))

class OrderInfo(db.Model):
	orderNumber = db.Column(db.Integer, primary_key=True, unique=True, index=True)
	employee_id = db.Column(db.Integer, nullable=True)
	item = db.Column(db.String(128), nullable=True)
	price = db.Column(db.Float, nullable=True)
	
