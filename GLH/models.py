from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum as SAEnum, Numeric
from enum import Enum
from extensions import db

# Utility for UTC timestamps
UTC_NOW = lambda: datetime.now(timezone.utc)

# ---------- Enums ----------
class Role(Enum):
    Customer = "customer"
    Admin    = "admin"
    Producer = "producer"

class OrderType(Enum):
    Collection = "collection"
    Delivery   = "delivery"

class Status(Enum):
    Pending   = "Pending"
    Confirmed = "Confirmed"
    Completed = "Completed"
    Cancelled = "Cancelled"

class Producers(Enum):
    bale_farm        = "bale_farm"
    ketil_farm       = "ketil_farm"
    featherdown_farm = "featherdown_farm"
    yang_farm        = "yang_farm"

# ---------- Models ----------
class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id       = db.Column(db.Integer, primary_key=True)
    role          = db.Column(SAEnum(Role), nullable=False)
    email         = db.Column(db.String(120), unique=True, index=True, nullable=False)
    phone_number  = db.Column(db.String(20), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    full_name     = db.Column(db.String(120))
    dob           = db.Column(db.Date)
    created_at    = db.Column(db.DateTime, nullable=False, default=UTC_NOW)
    last_login    = db.Column(db.DateTime)

    orders = db.relationship("Orders", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    """ verify if the provided password matches the stored hash. Returns true if correct. False otherwise"""
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Product(db.Model):
    __tablename__ = "products"
    product_id    = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    description   = db.Column(db.Text)
    price         = db.Column(Numeric(10, 2), nullable=False)
    stock         = db.Column(db.Integer, nullable=False, default=0)
    producer      = db.Column(SAEnum(Producers), nullable=False)
    created_at    = db.Column(db.DateTime, default=UTC_NOW)

    order_items = db.relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")

class Orders(db.Model):
    __tablename__  = "orders"
    order_id       = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    order_type     = db.Column(SAEnum(OrderType), nullable=False)
    status         = db.Column(SAEnum(Status), default=Status.Pending, nullable=False)
    order_total       = db.Column(Numeric(10, 2), nullable=False)
    order_date     = db.Column(db.DateTime, default=UTC_NOW)
    dc_date  = db.Column(db.DateTime)
    delivery_addr  = db.Column(db.String(255))

    user  = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id            = db.Column(db.Integer, primary_key=True)
    order_id      = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    product_id    = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    quantity      = db.Column(db.Integer, nullable=False, default=1)

    order   = db.relationship("Orders", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")