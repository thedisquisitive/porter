from app import app, db
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
    print("New access to index")
    print(current_user)
    return render_template('index.html', title='Home')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    print("New access to login")
    print(current_user)
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
    print("New access to logout")
    print(current_user)
    logout_user()
    return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    print("New access to registration")
    print(current_user)
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
    print("New access to orders")
    print(current_user)
    porders = db.session.scalars(sa.select(Order)).all()
    return render_template('orders.html', title='All Orders', orders=porders)

@app.route('/orders/<int:order_id>/')
@login_required
def order(order_id):
    print("New access to specific order")
    print(current_user)
    order = Order.query.get(order_id)
    creator = User.query.get(Order.query.get(order_id).user_id)
    return render_template('order.html', title='Order', order=order, creator=creator)

@app.route('/new_order', methods=['GET', 'POST'])
@app.route('/orders/new/', methods=['GET', 'POST'])
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
    print("New access to edit order")
    print(current_user)
    order = Order.query.get(order_id)
    form = EditOrderForm()
    if form.validate_on_submit():
        order.name = form.name.data
        order.description = form.description.data
        order.tracking_number = form.tracking_number.data
        order.date = form.date.data
        order.expected_delivery = form.expected_delivery.data
        order.price = form.price.data
        order.status = form.status.data
        db.session.commit()
        flash('Order edited!')
        return redirect(url_for('order', order_id=order_id))
    return render_template('edit_order.html', title='Edit Order', form=form, order=order)