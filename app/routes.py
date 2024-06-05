﻿from app import app, db
from app.models import User, Order
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from app.forms import LoginForm, RegistrationForm, NewOrderForm, EditOrderForm
import sqlalchemy as sa

@app.route('/')
@app.route('/index/')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('{{user.username}} registered successfully!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/orders/')
@app.route('/orders/all/')
@login_required
def orders():
    porders = db.session.scalars(sa.select(Order)).all()
    return render_template('orders.html', title='All Orders', orders=porders)

@app.route('/orders/<int:order_id>/')
@login_required
def order(order_id):
    order = Order.query.get(order_id)
    creator = User.query.get(Order.query.get(order_id).user_id)
    return render_template('order.html', title='Order', order=order, creator=creator)

@app.route('/new_order', methods=['GET', 'POST'])
@app.route('/orders/new/', methods=['GET', 'POST'])
@login_required
def new_order():
    form = NewOrderForm()  # Instantiate your form

    if form.validate_on_submit():
        # Create an Order object from form data
        user_id = current_user.id
        new_order = Order(
            name=form.name.data,
            description=form.description.data,
            tracking_number=form.tracking_number.data,
            date=form.date.data,  # Assuming form.date.data is a valid datetime
            expected_delivery=form.expected_delivery.data,  # Assuming form.expected_delivery.data is a valid datetime
            price=form.price.data,
            status=form.status.data,
            user_id=user_id
        )

        # Add the new order to the database session
        db.session.add(new_order)
        db.session.commit()

        # Redirect to a success page or another route
        return redirect(url_for('orders'))  # Replace with your desired route

    return render_template('new_order.html', form=form)

@app.route('/orders/<int:order_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order = Order.query.get(order_id)
    
    form = EditOrderForm()
    form.name.data = order.name
    form.description.data = order.description
    form.tracking_number.data = order.tracking_number
    form.date.data = order.date
    form.expected_delivery.data = order.expected_delivery
    form.price.data = order.price
    form.status.data = order.status

    if form.validate_on_submit():
        order.name = form.name.data
        order.description = form.description.data
        order.tracking_number = form.tracking_number.data
        order.date = form.date.data
        order.expected_delivery = form.expected_delivery.data
        order.price = form.price.data
        order.status = form.status.data
        try:
            print(form.errors)
            db.session.commit()
            flash('Order edited!')
        except Exception as e:
            flash('Error editing order: {}'.format(e))
        return redirect(url_for('order', order_id=order_id))
    return render_template('edit_order.html', title='Edit Order', form=form, order=order)

@app.route('/orders/<int:order_id>/delete/', methods=['GET', 'POST'])
@app.route('/delete/<int:order_id>/', methods=['GET', 'POST'])
@login_required
def delete_order(order_id):
    order = Order.query.get(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted!')
    return redirect(url_for('orders'))