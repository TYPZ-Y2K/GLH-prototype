from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum as SAEnum
from sqlalchemy import UniqueConstraint
from enum import Enum
from extensions import db

UTC_NOW = lambda: datetime.now(timezone.utc)

# ---------- Enums ----------

class role(Enum):
    Customer = "customer"
    Admin    = "admin"
    Producer = "producer"

class order_type(Enum):
    Collection = "collection"
    Delivery   = "Delivery"

class Status(Enum):
    Pending   = "Pending"
    Confirmed = "Confirmed"
    Completed = "Completed"
    Cancelled = "Cancelled"

class producers(Enum):
    bale_farm         = "bale_farm"
    ketil_farm        = "ketil_farm"
    featherdown_farm  =  "featherdown farm"
    yang_farm         = "yang farm"

    

# ---------- Models ----------
class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id       = db.Column(db.Integer, primary_key=True)
    role          = db.Column(db.String(16), nullable=False)  # "Customer" | "Admin"
    email         = db.Column(db.String(120), unique=True, index=True, nullable=False)
    phone_number  = db.Column(db.String(20), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    full_name     = db.Column(db.String(120))
    dob           = db.Column(db.Date)
    created_at    = db.Column(db.DateTime, nullable=False, default=UTC_NOW)
    last_login    = db.Column(db.DateTime)

    orders      = db.relationship("orders", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Orders(db.Model):
    __tablename__  = "Orders"
    id             = db.Column(db.Integer, primary_key=True)
    Order_id       = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    order_type     = db.Column(SAEnum(order_type), nullable=False)
    status         = db.Column(SAEnum(Status), nullable=False, default=Status.Available)
    order_date     = db.Column(db.DateTime, nullable=False)
    ordered_at     = db.Column(db.DateTime, default=UTC_NOW, nullable=False)
    total_price    = db.Column(db.Integer, nullable=True)  # or Numeric(10,2)


    user = db.relationship("user", back_populates="orders", lazy="joined")
    order_items      = db.relationship("order_items", back_populates="orders", cascade="all, delete-orphan", lazy="dynamic")


class Order_items (db.Model):
    __tablename__= "Order items"
    OrderItem_id = db.Column(db.Integer, primary_key=True)
    Order_id     =  db.Column(db.Integer, db.ForeignKey("Orders.Order_id"), nullable=False)
    quantity     = db.Column(db.Integer, nullable=False)
    unit_price   = db.Column(db.Integer, nullable=False) 

    Orders = db.relationship("Orders", back_populates="Order_items ", lazy="joined")
   
class Farmers_Market(db.Model):
    __tablename__ = "farmers_market"
    produce_id    = db.Column(db.Integer, primary_key=True)
    product_name  = db.Column(db.String(120), nullable=False)
    user_id       = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    product       = db.Column(db.String(120), nullable=False)
    price         = db.Column(db.Integer, nullable=False)
    source        = db.Column(SAEnum(producers))
    stock         = db.Column(db.Integer, nullable=False)