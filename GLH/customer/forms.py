# customer/forms.py
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class CheckoutForm(FlaskForm):
    # make exclusive list of options fot the user to choose from
    order_type = RadioField(
        "Order Type",
        choices = [("collection", "collection"), ("delivery", "delivery")],
        default = "collection",
        validators=[DataRequired()],
    )

    delivery_addr = StringField(
        "Delivey Address",
        validators=[Length(max=255)],
    )
    
    submit = SubmitField("Place Order")

    def validate_delivery_addr(self, field):
        """ Require address only when delivery is selected."""
        if self.order_type.data == "delivery" and not field.data.strip():
            raise ValidationError("Please enter a delivery address.")

