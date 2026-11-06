from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    orders = db.relationship("Order", backref="customer", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(250))

    products = db.relationship("Product", backref="category", lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)

    price = db.Column(db.Numeric(10, 2), nullable=False)

    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True, nullable=False)

    # Serving and nutritional information
    serving_size_g = db.Column(db.Numeric(8, 2), nullable=True)
    protein_g = db.Column(db.Numeric(8, 2), nullable=True)
    carbs_g = db.Column(db.Numeric(8, 2), nullable=True)
    calories_kcal = db.Column(db.Numeric(8, 2), nullable=True)
    fibre_g = db.Column(db.Numeric(8, 2), nullable=True)

    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=False
    )

    order_items = db.relationship("OrderItem", backref="product", lazy=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(30), unique=True, nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="Pending", nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    items = db.relationship(
        "OrderItem", backref="order", lazy=True, cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    order_id = db.Column(
        db.Integer, db.ForeignKey("order.id"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
