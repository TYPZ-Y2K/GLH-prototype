from datetime import datetime, timezone
from flask import current_app,request, render_template, redirect, url_for, flash, session, make_response
from flask_login import login_user, current_user, login_required, logout_user
from . import customer_bp as bp  #  Blueprint created in customer/__init__.py;  its name is "customer"

@bp.route("/Dashboard")
def customer_dashboard():
    return render_template("customer/customer_dashboard.html")



@bp.route("/Farmers-Market")
def Farmers_Market():
    return render_template("customer/Farmers-Market.html")
