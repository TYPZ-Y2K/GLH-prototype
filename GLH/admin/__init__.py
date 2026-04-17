# auth/__init__.py
from flask import Blueprint
admin_bp = Blueprint("admin", __name__)
from . import routes  # <-- This is required so routes are registered