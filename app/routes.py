import os
from flask import render_template, flash, redirect, request, url_for, session
from app import app, mail, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import OrderInfo, PaymentInfo, User
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_mail import Message
from random import randint
import random
import string
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import func, asc, desc

@app.route('/',methods=['GET', 'POST'])
@app.route('/login',methods=['GET', 'POST'])
def login():
	currentUsers = User.query.all()
	if len(currentUsers) == 0:
		user = User(id = 4020)
		db.session.add(user)
		user = User(id = 1234)
		db.session.add(user)
		user = User(id = 6022)
		db.session.add(user)
		db.session.commit()
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=form.employee_id.data).first()
		if user is None:
			flash('Invalid Employee Id')
			return redirect(url_for('login'))
		else:
			login_user(user)
			print(form.employee_id.data)
			return redirect(url_for('order_entry'))
	return render_template('employee_login.html', title='Login Page', form=form)
@app.route('/order_history', methods=['GET', 'POST'])
@login_required
def order_history():
	form = TableToCharge()
	if form.validate_on_submit():
		order = OrderInfo.query.filter_by(table = form.table.data)
		order_num = order.first()
		if order_num is None:
			flash("Invalid Table")
		else:
			openOrder = order.filter_by(billSent="Open")
			if openOrder is None:
				flash("Bill has already been sent")
				return redirect(url_for('order_history'))
			current_user.currentCustomerEmail = form.email.data
			body = "Please click this link to pay your bill: 127.0.0.1:5000/payment:{}".format(int(order_num.order_num))
			msg = Message("Here is your bill",
				sender=app.config.get("MAIL_USERNAME"),
	 			recipients=[form.email.data],
	 			body = body)
			mail.send(msg)
			flash("Email has been sent")
			orders = OrderInfo.query.filter_by(table = form.table.data).all()
			for order in orders:
				if order.billSent == "Open":
					order.billSent = "Sent";
			db.session.commit()
			return redirect(url_for('order_history'))
	return render_template('/order_history.html', title='Order History', form=form, orders=OrderInfo.query.filter_by(employee_id=current_user.id).order_by(OrderInfo.order_num).all(),employee_id=current_user.id)

@app.route('/order_entry', methods=['GET', 'POST'])
@login_required
def order_entry():
	form = OrderEntryForm()
	if form.validate_on_submit():
		
		info = OrderInfo(table=form.table.data,item=form.item.data, price=form.price.data)
		orders = OrderInfo.query.all()
		if len(orders)==0:
			info.id = 0
			info.order_num = 0
	
		else:
			info.id = orders[-1].id + 1
			# tableQuery = OrderInfo.query.filter_by(table = form.table.data).order_by(desc(OrderInfo.order_num))
			maxOrderNum = db.session.query(func.max(OrderInfo.order_num)).scalar()
			# tableNum = tableQuery.first()
			maxOrderNumForTable = OrderInfo.query.filter_by(table=form.table.data).order_by(desc(OrderInfo.order_num)).first()
			if maxOrderNumForTable is not None:
				if maxOrderNumForTable.billSent == "Open":
					info.order_num = maxOrderNumForTable.order_num
				else:
					info.order_num = maxOrderNum + 1
			else:
				info.order_num = maxOrderNum + 1

		info.billSent = "Open"
		info.employee_id = current_user.id
		db.session.add(info)
		db.session.commit()
		flash('Order Added')
		return redirect(url_for('order_entry'))
	return render_template('/order_entry.html', title='Order Entry', form=form, employee_id=current_user.id)

@app.route('/payment_history', methods=['GET'])
@login_required
def payment_history():
	return render_template('/payment_history.html', payments=PaymentInfo.query.all(),employee_id=current_user.id)
#add payment id to handle multiple users?
@app.route('/payment:<int:order_num>', methods=['GET', 'POST'])
def payment(order_num):
	print(order_num)
	orders = OrderInfo.query.filter_by(order_num=order_num).all()
	if len(orders) == 0:
		return redirect(url_for('repay_error'))
	else:
		price = 0
		for order in orders:
			price += order.price

		form = PaymentForm()
		if form.validate_on_submit():
			print('is valid')
			info = PaymentInfo(name=form.name.data, cardtype=form.cardtype.data, 
				card_num=form.cardnumber.data, card_exp=form.card_exp.data,
				address=form.address.data, city=form.city.data, state=form.state.data, 
				zip_code=form.zip_code.data)
			if form.tip.data == None:
				form.tip.data = 0
			info.orderPrice = price + form.tip.data
			info.employee_id = orders[0].employee_id
			email = User.query.filter_by(id = info.employee_id).first().currentCustomerEmail
			print(email)
			
			body = "Thank you for your business {}, here is your reciept:\r\n Order Number: {} \r\n".format(form.name.data, order_num)
			count = 1
			for order in orders:
				order.billSent = "Closed"

				body += "{}. item: {} price: {}\r\n".format(count, order.item, order.price)
				count = count + 1 

			body += "\r\n Tip: {}".format(form.tip.data)
			body += "\r\nTotal: {}".format(info.orderPrice)

			msg = Message("Here is your reciept",
				sender=app.config.get("MAIL_USERNAME"),
				recipients=[email],
				body = body)
			mail.send(msg)

			db.session.add(info)
			db.session.commit()
			return redirect(url_for('payment_confirmation'))
	return render_template('payment.html', title='payment', form=form, orders=orders, price=price)

@app.route("/payment_confirmation", methods=['GET'])
def payment_confirmation():
	return render_template('/payment_confirmation.html', title='Payment Confirmation')

@app.route("/repay_error", methods=['GET'])
def repay_error():
	return render_template('/repay_error.html', title='Repay Error')
	
@app.route("/logout", methods=['GET', 'POST'])
def logout():
	flash('Successfully logged out user {}'.format(current_user.id))
	logout_user()
	return redirect('login')

@app.route("/clear_order_history")
def clearOrders():
	OrderInfo.query.delete()
	db.session.commit()
	return redirect('order_history')

@app.route("/clear_payment_history")
def clearPayments():
	PaymentInfo.query.delete()
	db.session.commit()
	return redirect('payment_history')

