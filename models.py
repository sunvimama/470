from datetime import datetime
from TechBazar import db  # adjust import based on your structure

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Assuming you have a User model
    full_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    discount_applied = db.Column(db.Float, default=0)  # Store discount applied
    final_price = db.Column(db.Float, nullable=False)  # Final price after applying discount
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon.id'))  # Relate to Coupon model
    status = db.Column(db.String(20), default='Processing')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True)
    coupon = db.relationship('Coupon', backref='orders', lazy=True)

    def apply_coupon(self, coupon_code):
        """Apply a coupon to the order."""
        coupon = Coupon.query.filter_by(code=coupon_code).first()
        if coupon and coupon.is_valid():
            self.discount_applied = self.total_price * (coupon.discount_percentage / 100)
            self.final_price = self.total_price - self.discount_applied
            self.coupon_id = coupon.id
        else:
            self.discount_applied = 0
            self.final_price = self.total_price

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # Assuming you have a Product model
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)  # Coupon code
    discount_percentage = db.Column(db.Float, nullable=False)  # Discount in percentage
    expiration_date = db.Column(db.DateTime)  # Optional: Expiry date of coupon

    def is_valid(self):
        """Check if the coupon is valid (not expired)"""
        if self.expiration_date:
            return self.expiration_date > datetime.now()
        return True  # No expiration date means it's always valid

class ReturnRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending')  # Pending, Approved, Rejected, Refunded
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RefundStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    return_id = db.Column(db.Integer, db.ForeignKey('return_request.id'), nullable=False)
    refunded = db.Column(db.Boolean, default=False)
    refund_date = db.Column(db.DateTime)
    amount = db.Column(db.Float)


