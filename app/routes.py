import os
from flask import render_template, flash, redirect, request, url_for, session
from app import app, mail, db
from app.forms import *
#from flask_login import current_user, login_user, logout_user, login_required
from app.models import OrderInfo, PaymentInfo
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

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		info = LoginForm(employee_id = form.employee_id.data)
		print(form.employee_id.data)
		return redirect(url_for('order_entry'))
	return render_template('employee_login.html', title='Login Page', form=form)
@app.route('/order_history', methods=['GET', 'POST'])
def order_history():
	return render_template('/order_history.html', title='Order History', orders=OrderInfo.query.all())

@app.route('/order_entry', methods=['GET', 'POST'])
def order_entry():
	form = OrderEntryForm()
	if form.validate_on_submit():
		info = OrderEntryForm(order_num=form.order_num.data, employee_id=form.employee_id.data,
			item=form.item.data, price=form.price.data)
		print(form.order_num.data)
		db.session.add(info)
		db.session.commit()
		flash('Order Added')
	return render_template('/order_entry.html', title='Order Entry', form=form)

#add payment id to handle multiple users?
@app.route('/payment', methods=['GET', 'POST'])
def payment():
	form = PaymentForm()
	if form.validate_on_submit():
		info = PaymentForm(name=form.name.data, cardtype=form.cardtype.data, 
			cardnumber=form.cardnumber.data, card_exp=form.card_exp.data, card_cvv=form.card_cvv.data,
			address=form.address.data, city=form.city.data, state=form.state.data, 
			zip_code=form.zip_code.data)
		db.session.add(info)
		db.session.commit()
		flash('Payment Saved')
		return "<p>Thank You</p>"
	return render_template('payment.html', title='Order Entry', form=form)
