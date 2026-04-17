# auth/__init__.py
from flask import Blueprint
public_bp = Blueprint("public", __name__)
from . import routes  # <-- This is required so routes are registered