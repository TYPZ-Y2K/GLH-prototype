from datetime import datetime, timezone
from flask import current_app,request, render_template, redirect, url_for, flash, session, make_response
from flask_login import login_user, current_user, login_required, logout_user
from . import public_bp as bp  #  Blueprint created in public/__init__.py;  its name is "public"


@bp.route("/about us")
def about_us():
    return render_template("public/about-us.html")

@bp.route("/privacy")
def privacy():
    return render_template("public/privacy.html")

@bp.route("/our-products")
def our_products():
    return render_template("public/our-products.html")