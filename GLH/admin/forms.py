# admins/forms.py
from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, DecimalField, IntegerField,
    SelectField, SubmitField, PasswordField
)
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from models import Producers 

class ProductForm(FlaskForm): # form allows products to be added or edited
    """ Add or edit a product"""
    name = StringField(
        "product Name",
        validators=[DataRequired(), Length(min=2, max=120)], 
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired(), Length(max=500)],
    )
    price = DecimalField(
        "Price (£)",
        validators=[DataRequired(), NumberRange(min=0.01, message="Price must be positive")],
    )
    stock = IntegerField(
        "stock",
        validators=[DataRequired(), NumberRange(min=0, message="stock cannot be negative")]
    )
    producer = SelectField(
        "Producer / Farm ",
        choices=[(p.value, p.value.replace("_"," ").title()) for p in Producers],
        validators=[DataRequired()],
    )
    submit = SubmitField("Save Product")

class DeleteProductForm(FlaskForm):
    """Confirm deletion with password"""
    password = PasswordField(
        "Enter your password to confirm",
        validators=[DataRequired()],
    )
    delete_submit = SubmitField("Delete Product")

class UpdateStockForm(FlaskForm):
    """Quick stock update"""
    stock = IntegerField(
        "New stock level",
        validators=[DataRequired(), NumberRange(min=0, message="Stock cannot be negative")]
    )