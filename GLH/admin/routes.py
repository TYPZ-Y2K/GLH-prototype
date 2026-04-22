# admin/routes.py
from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models import Product, Orders, Status, Producers, Role
from extensions import db
from .forms import ProductForm, DeleteProductForm, UpdateStockForm
from . import admin_bp as bp


# ── Role guard decorator ──
def admin_required(f):
    """Block access unless user is Admin or Producer."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in.", "error")
            return redirect(url_for("auth.login"))
        if current_user.role not in (Role.Admin, Role.Producer):
            flash("Access denied.", "error")
            return redirect(url_for("customer.customer_dashboard"))
        return f(*args, **kwargs)
    return decorated


# ── Dashboard overview ──
@bp.route("/dashboard")
@login_required
@admin_required
def admin_dashboard():
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.stock < 5).count()
    pending_orders = Orders.query.filter_by(status=Status.Pending).count()
    confirmed_orders = Orders.query.filter_by(status=Status.Confirmed).count()

    recent_orders = (
        Orders.query
        .order_by(Orders.order_date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/admin_dashboard.html",
        total_products=total_products,
        low_stock=low_stock,
        pending_orders=pending_orders,
        confirmed_orders=confirmed_orders,
        recent_orders=recent_orders,
    )


# ── Produce control (list + add) ──
@bp.route("/products", methods=["GET", "POST"])
@login_required
@admin_required
def product_list():
    form = ProductForm()

    if form.validate_on_submit():
        product = Product(
            name=form.name.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            price=form.price.data,
            stock=form.stock.data,
            producer=Producers(form.producer.data),
        )
        db.session.add(product)
        db.session.commit()
        flash(f"'{product.name}' added successfully.", "success")
        return redirect(url_for("admin.product_list"))

    if form.errors:
        for field, errors in form.errors.items():
            for err in errors:
                flash(err, "error")

    products = Product.query.order_by(Product.name.asc()).all()
    return render_template("admin/Produce-control.html", products=products, form=form)


# ── Edit product ──
@bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("admin.product_list"))

    form = ProductForm(obj=product)
    # Pre-select the current producer in the dropdown
    if request.method == "GET":
        form.producer.data = product.producer.value

    if form.validate_on_submit():
        product.name = form.name.data.strip()
        product.description = form.description.data.strip() if form.description.data else None
        product.price = form.price.data
        product.stock = form.stock.data
        product.producer = Producers(form.producer.data)
        db.session.commit()
        flash(f"'{product.name}' updated.", "success")
        return redirect(url_for("admin.product_list"))

    return render_template(
        "admin/edit-product.html",
        product=product,
        form=form,
    )


# ── Delete product (password required) ──
@bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("admin.product_list"))

    form = DeleteProductForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.password.data):
            flash("Incorrect password.", "error")
            return redirect(url_for("admin.product_list"))

        name = product.name
        db.session.delete(product)
        db.session.commit()
        flash(f"'{name}' deleted.", "success")
    else:
        flash("Please confirm with your password.", "error")

    return redirect(url_for("admin.product_list"))


# ── Quick stock update ──
@bp.route("/products/<int:product_id>/stock", methods=["POST"])
@login_required
@admin_required
def update_stock(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("admin.product_list"))

    form = UpdateStockForm()
    if form.validate_on_submit():
        product.stock = form.stock.data
        db.session.commit()
        flash(f"Stock for '{product.name}' updated to {product.stock}.", "success")
    else:
        for err in form.stock.errors:
            flash(err, "error")

    return redirect(url_for("admin.product_list"))


# ── View all orders ──
@bp.route("/orders")
@login_required
@admin_required
def view_orders():
    filter_type = request.args.get("filter", "all")

    query = Orders.query.order_by(Orders.order_date.desc())

    if filter_type == "upcoming":
        query = query.filter(Orders.status.in_([Status.Pending, Status.Confirmed]))
    elif filter_type == "past":
        query = query.filter(Orders.status.in_([Status.Completed, Status.Cancelled]))

    orders = query.all()
    return render_template("admin/orders.html", orders=orders, filter_type=filter_type)


# ── Update order status ──
@bp.route("/orders/<int:order_id>/status", methods=["POST"])
@login_required
@admin_required
def update_order_status(order_id):
    order = db.session.get(Orders, order_id)
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("admin.view_orders"))

    new_status = request.form.get("status")
    valid = {s.value: s for s in Status}

    if new_status not in valid:
        flash("Invalid status.", "error")
    else:
        order.status = valid[new_status]
        db.session.commit()
        flash(f"Order #{order.order_id} marked as {new_status}.", "success")

    return redirect(url_for("admin.view_orders"))
