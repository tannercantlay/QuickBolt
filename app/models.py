#from app import db

class Order(db.Model):
	orderNumber = db.Column(db.Integer, primary_key=True, unique=True, index=True)
	card_num = db.Column(db.String(128), nullable=True)
    card_exp = db.Column(db.String(128), nullable=True)
    cardtype = db.Column(db.String(1), nullable=True)
    name = db.Column(db.String(128), nullable=True)
    address = db.Column(db.String(128), nullable=True)
	city = db.Column(db.String(128), nullable=True)
	state = db.Column(db.String(128), nullable=True) 
	zip_code = db.Column(db.String(128), nullable=True)