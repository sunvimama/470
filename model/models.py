from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime


db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Nid = db.Column(db.Integer, unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', backref='reviews')
    product = db.relationship('Product', backref='reviews')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_number = db.Column(db.String(20), unique=True)
    status = db.Column(db.String(50), nullable=False, default='Processing')
    order_date = db.Column(db.DateTime, default=db.func.now())
    delivery_date = db.Column(db.DateTime, nullable=True)
    total_price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    coupon_code = db.Column(db.String(50), nullable=True)
    discount_amount = db.Column(db.Float, nullable=True)

    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship('Product')

class Coupon(db.Model):
    __tablename__ = 'coupon'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_amount = db.Column(db.Float, nullable=False)
    is_percentage = db.Column(db.Boolean, default=False)
    valid_from = db.Column(db.DateTime, nullable=True)
    valid_to = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    user = db.relationship('User', backref='wishlist_items')
    product = db.relationship('Product')

class EmiPlan(db.Model):
    __tablename__ = 'emi_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    emi_duration = db.Column(db.Integer, nullable=False)
    emi_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='emi_plans')
    order = db.relationship('Order', backref='emi_plans')

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notification_type = db.Column(db.String(50))  # 'wishlist', 'restock', 'order', 'emi', etc.
    related_id = db.Column(db.Integer)  # ID of related product/order/etc.

    user = db.relationship('User', backref='notifications')

class UserProductView(db.Model):
    __tablename__ = 'user_product_views'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    view_count = db.Column(db.Integer, default=1)
    last_viewed = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='viewed_products')
    product = db.relationship('Product')

class ReturnRequest(db.Model):
    __tablename__ = 'return_requests'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='return_requests')
    order = db.relationship('Order', backref='return_requests')

class RefundStatus(db.Model):
    __tablename__ = 'refund_status'
    id = db.Column(db.Integer, primary_key=True)
    return_id = db.Column(db.Integer, db.ForeignKey('return_requests.id'), nullable=False)
    refunded = db.Column(db.Boolean, default=False)
    refund_date = db.Column(db.DateTime, nullable=True)
    amount = db.Column(db.Float, nullable=False)

    return_request = db.relationship('ReturnRequest', backref='refund_status')