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
        .all()
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
        return redirect(url_for("customer.Farmers_Market"))  # Redirect back to basket page

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
# ── Place order (simulated payment) ──
@bp.route("/place-order", methods=["POST"])
@login_required
def place_order():
    basket = session.get("basket", {})
    if not basket:
        flash("Your basket is empty.", "error")
        return redirect(url_for("customer.Farmers_Market"))

    order_type_str = request.form.get("order_type", "collection")
    delivery_addr = request.form.get("delivery_addr", "").strip()

    if order_type_str == "delivery" and not delivery_addr:
        flash("Please enter a delivery address.", "error")
        return redirect(url_for("customer.checkout"))

    otype = OrderType.Delivery if order_type_str == "delivery" else OrderType.Collection
    dc_date = datetime.now(timezone.utc) + timedelta(days=3)

    order = Orders(
        user_id=current_user.user_id,
        order_type=otype,
        status=Status.Pending,
        dc_date=dc_date,
        delivery_addr=delivery_addr if otype == OrderType.Delivery else None,
    )
    db.session.add(order)
    db.session.flush()

    for pid_str, qty in basket.items():
        product = db.session.get(Product, int(pid_str))
        if product and product.stock >= qty:
            product.stock -= qty
            db.session.add(OrderItem(
                order_id=order.order_id,
                product_id=product.product_id,
                quantity=qty,
            ))
        else:
            db.session.rollback()
            flash(f"Not enough stock for {product.name if product else 'item'}.", "error")
            return redirect(url_for("customer.checkout"))

    db.session.commit()
    session.pop("basket", None)
    flash("Order placed successfully!", "success")
    return redirect(url_for("customer.customer_dashboard"))


# ── Cancel order ──
@bp.route("/cancel-order/<int:order_id>", methods=["POST"])
@login_required
def cancel_order(order_id):
    order = Orders.query.filter_by(order_id=order_id, user_id=current_user.user_id).first()
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("customer.customer_dashboard"))

    if order.status not in (Status.Pending, Status.Confirmed):
        flash("This order cannot be cancelled.", "error")
        return redirect(url_for("customer.customer_dashboard"))

    for item in order.items:
        item.product.stock += item.quantity

    order.status = Status.Cancelled
    db.session.commit()
    flash("Order cancelled.", "success")
    return redirect(url_for("customer.customer_dashboard"))