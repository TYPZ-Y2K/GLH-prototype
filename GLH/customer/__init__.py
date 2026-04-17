# auth/__init__.py
from flask import Blueprint
customer_bp = Blueprint("customer", __name__)
from . import routes  # <-- This is required so routes are registered