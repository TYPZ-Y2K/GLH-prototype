from datetime import datetime, timezone, timedelta
from flask import current_app, request, render_template, redirect, url_for, flash, session
from flask_login import current_user, login_required
from models import Orders, OrderItem, Product, Status, OrderType
from extensions import db
from .forms import CheckoutForm
from . import customer_bp as bp

@bp.route("/Dashboard")
@login_required
def customer_dashboard():
    now = datetime.now(timezone.utc)

    # upcoming = pending or confirmed orders
    upcoming = ( 
        Orders.query
        .filter_by(user_id=current_user.user_id)
        .filter(Orders.status.in_([Status.Pending, Status.Confirmed]))
        .order_by(Orders.dc_date.asc())
        .all()
    )

    # Previous = completed or cancelled
    previous = (
        Orders.query
        .filter_by(user_id=current_user.user_id)
        .filter(Orders.status.in_({Status.Completed, Status.Cancelled}))
        .order_by(Orders.order_date.asc())
    )

    return render_template(
        "customer/customer_dashboard.html",
        upcoming=upcoming,
        previous=previous,
    )

@bp.route("/Farmers-Market")
@login_required
def Farmers_Market():
    products = Product.query.filter(Product.stock > 0).all()
    return render_template("customer/Farmers-Market.html", products=products)

@bp.route("/checkout")
@login_required
def checkout():
    basket = session.get("basket", {})
    if not basket:
        flash("your basket is empty.", "error")

        items = []
        total = 0
        for pid_str, qty in basket.items():
            product = db.session.get(Product, int(pid_str))
            if product:
                subtotal = float(product.price) * qty
                total += subtotal
                items.append({"product": product, "qty": qty, "subtotal": subtotal})
        
        form = CheckoutForm()
        return render_template("customer/checkout.html", items=items, total=total, form=form)

# ── Basket helpers ──

@bp.route("/add-to-basket/<int:product_id>", methods=["POST"])
@login_required
def add_to_basket(product_id):
    product = db.session.get(Product, product_id)
    if not product or product.stock < 1:
        flash("Product unavailable.", "error")
        return redirect(url_for("customer.Farmers_Market"))
    
    basket = session.get("basket", {})
    key = str(product_id)
    basket[key] = basket.get(key, 0) + 1
    session["basket"] = basket
    flash(f"{product.name} added to basket.", "success")
    return redirect(url_for("customer.Farmers_Market"))

@bp.route("/remove-from-basket/<int:product_id>", methods=["POST"])
@login_required
def remove_from_basket(product_id):
    basket = session.get("basket", {})
    key = str(product_id)
    if key in basket:
        del basket[key]
        session["basket"] = basket
        flash("Item remove.", "success")
        return redirect(url_for("customer.checkout"))

