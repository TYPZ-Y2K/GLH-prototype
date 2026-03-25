# auth/__init__.py
from flask import Blueprint
bp = Blueprint("customer", __name__, template_folder="/templates")
from . import routes  # <-- This is required so routes are registered