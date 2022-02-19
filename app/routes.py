import os
from flask import render_template, flash, redirect, request, url_for, session
from app import app, mail 
#db
from app.forms import *
#from flask_login import current_user, login_user, logout_user, login_required
#from app.models import User, Book, Promotion, Order, ListItem
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_mail import Message
from random import randint
import random
import string
from datetime import date, datetime
from decimal import Decimal

# msg = Message("Sup Buddy",
#  		sender=app.config.get("MAIL_USERNAME"),
#        recipients=["tannercantlay@gmail.com"],
#        body = "Bitch")
# mail.send(msg)

@app.route('/')
@app.route('/index')
def index():
	return "<p>Hello World</p>"
	#render_template(templatefile, title='Login Page')
def order_history():
	return "<p>order_history</p>"
	#render_template(templatefile, title='Order History')

@app.route('/order_entry')
def order_entry():
	return "<p>Order Entry</p>"
	#render_template(templatefile, title='Order Entry')

#add payment id to handle multiple users?
@app.route('/payment')
def payment():
	form = PaymentForm()
	if form.validate_on_submit():
		info = PaymentForm(name=form.name.data, cardtype=form.cardtype.data, 
			cardnumber=form.cardnumber.data, card_exp=form.card_exp.data, 
			address=form.address.data, city=form.city.data, state=form.state.data, 
			zip_code=form.zip_code.data)
		# db.session.add(info)
  #       db.session.commit()
  #       flash('Payment Saved')
  #       return redirect('thankyoupage')
	return "<p>payment</p>"
	#render_template(templatefile, title='Order Entry')
