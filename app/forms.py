from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User
from app import db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username: str) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email: str) -> None:
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class NewOrderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ticket_number = StringField('Ticket Number', validators=[DataRequired()])
    description = StringField('Description', widget=TextArea(), validators=[DataRequired()])
    tracking_number = StringField('Tracking Number', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    expected_delivery = DateField('Expected Delivery', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Add Order')

class EditOrderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ticket_number = StringField('Ticket Number', validators=[DataRequired()])
    description = StringField('Description', widget=TextArea(), validators=[DataRequired()])
    tracking_number = StringField('Tracking Number', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    expected_delivery = DateField('Expected Delivery', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Submit Changes')