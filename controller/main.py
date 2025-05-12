from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add the root project directory to the path

from model.models import db, User, Product, Review, Order, OrderItem, Coupon, Wishlist, EmiPlan, Notification, UserProductView, ReturnRequest, RefundStatus


import random
import string
import stripe

load_dotenv()

app = Flask(__name__, template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'))

app.secret_key = "sunvi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/etech'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------ Models ------------------

print("Templates folder is at:", os.path.abspath('templates'))
import os
print(f"Template file exists: {os.path.exists('templates/home.html')}")

# ------------------ Auth & Admin Utils ------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access only.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
# Notification Utilities
def create_notification(user_id, message, notification_type, related_id=None):
    """Create a new notification for a user"""
    notification = Notification(
        user_id=user_id,
        message=message,
        notification_type=notification_type,
        related_id=related_id
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def get_unread_notifications_count(user_id):
    """Get count of unread notifications for a user"""
    return Notification.query.filter_by(user_id=user_id, is_read=False).count()

def get_user_notifications(user_id, limit=5):
    """Get recent notifications for a user"""
    return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(limit).all()

def mark_notifications_as_read(user_id, notification_ids=None):
    """Mark notifications as read (specific or all)"""
    query = Notification.query.filter_by(user_id=user_id, is_read=False)
    if notification_ids:
        query = query.filter(Notification.id.in_(notification_ids))
    query.update({'is_read': True})
    db.session.commit()
# ------------------ Routes ------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/product-display')
def product_display():
    products = Product.query.all()
    return render_template('product_display.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(Email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            new_user = User(
                Name=request.form['Name'],
                Email=request.form['Email'],
                Nid=int(request.form['Nid']),
                phone=int(request.form['phone']),
                password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
@app.route('/order/<int:order_id>')
@login_required
def view_order(order_id):
    # If admin, allow viewing any order
    if current_user.is_admin:
        order = Order.query.filter_by(id=order_id).first_or_404()
    else:
        # Regular users can only view their own orders
        order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()

    # Get order items
    order_items = OrderItem.query.filter_by(order_id=order.id).all()

    return render_template('order_details.html', order=order, order_items=order_items)

@app.route('/admin/update_order_status/<int:order_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    print(f"DEBUG: Accessing update_order_status for order_id={order_id}, current status={order.status}")

    if request.method == 'POST':
        new_status = request.form.get('status')
        print(f"DEBUG: POST request received with new_status={new_status}")
        if new_status:
            old_status = order.status
            order.status = new_status
            try:
                db.session.commit()
                print(f"DEBUG: Order status updated from {old_status} to {new_status}")
                flash(f"Order status updated to {new_status}.", "success")
            except Exception as e:
                db.session.rollback()
                print(f"DEBUG: Error updating order status: {str(e)}")
                flash(f"Error updating order status: {str(e)}", "danger")
            return redirect(url_for('admin_orders'))

    return render_template('admin/update_order_status.html', order=order)


# ------------------ Admin Dashboard & Product Management ------------------

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_products = Product.query.count()
    return render_template('admin/dashboard.html', total_users=total_users, total_products=total_products)

@app.route('/admin/products')
@login_required
@admin_required
def admin_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        try:
            # Create the new product
            product = Product(
                name=request.form['name'],
                description=request.form['description'],
                price=float(request.form['price']),
                stock=int(request.form['stock']),
                image_url=request.form['image_url']
            )
            db.session.add(product)
            db.session.commit()

            # Notify all users about the new product
            users = User.query.all()
            for user in users:
                create_notification(
                    user_id=user.id,
                    message=f"New product added: {product.name}",
                    notification_type='new_product',
                    related_id=product.id
                )

            flash('Product added successfully and notifications sent!', 'success')
            return redirect(url_for('admin_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {str(e)}', 'danger')
    return render_template('admin/add_product.html')


@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        try:
            old_stock = product.stock
            new_stock = int(request.form['stock'])

            product.name = request.form['name']
            product.description = request.form['description']
            product.price = float(request.form['price'])
            product.stock = new_stock
            product.image_url = request.form['image_url']

            # Check if product was restocked
            if old_stock == 0 and new_stock > 0:
                # Find all users who have this in their wishlist
                wishlist_users = Wishlist.query.filter_by(product_id=product.id).all()
                for item in wishlist_users:
                    create_notification(
                        user_id=item.user_id,
                        message=f"{product.name} is back in stock!",
                        notification_type='restock',
                        related_id=product.id
                    )

            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', 'danger')
    return render_template('admin/edit_product.html', product=product)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'danger')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@login_required
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()

    total_sales = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    total_orders = len(orders)
    completed_orders = Order.query.filter_by(status='Delivered').count()
    pending_orders = Order.query.filter(Order.status != 'Delivered').count()

    return render_template('admin/admin_orders.html', orders=orders, total_sales=total_sales, total_orders=total_orders,
                           completed_orders=completed_orders, pending_orders=pending_orders)

# ------------------ Review ------------------

@app.route('/product/<int:product_id>/reviews', methods=['GET', 'POST'])
@login_required
def product_reviews(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.timestamp.desc()).all()

    if request.method == 'POST':
        content = request.form.get('content')
        rating = int(request.form.get('rating'))

        if not content or not rating:
            flash("Review and rating are required.", "warning")
        else:
            new_review = Review(content=content, rating=rating, user_id=current_user.id, product_id=product_id)
            db.session.add(new_review)
            db.session.commit()
            flash("Your review has been posted!", "success")
            return redirect(url_for('product_reviews', product_id=product_id))

    return render_template('review.html', product=product, reviews=reviews)

# ------------------ Product Search & Filtering ------------------

@app.route('/search')
def search_products():
    brand = request.args.get('brand')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    availability = request.args.get('availability')

    products = Product.query

    if brand:
        products = products.filter(Product.name.ilike(f"%{brand}%"))
    if min_price is not None:
        products = products.filter(Product.price >= min_price)
    if max_price is not None:
        products = products.filter(Product.price <= max_price)
    if availability == 'in_stock':
        products = products.filter(Product.stock > 0)
    elif availability == 'out_of_stock':
        products = products.filter(Product.stock <= 0)

    filtered_products = products.all()
    return render_template('search_results.html', products=filtered_products)

# ------------------ Order Tracking & History ------------------

@app.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    return render_template('order_history.html', orders=orders)

# ------------------ Context Processor ------------------

@app.context_processor
def inject_products():
    products = Product.query.all()
    return dict(products=products)






@app.route('/wishlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    existing_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not existing_item:
        new_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(new_item)

        # Create notification
        create_notification(
            user_id=current_user.id,
            message=f"You added {product.name} to your wishlist",
            notification_type='wishlist',
            related_id=product.id
        )

        db.session.commit()
        flash('Added to wishlist!', 'success')
    else:
        flash('Item already in wishlist.', 'info')
    return redirect(url_for('shop'))

@app.route('/wishlist/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Removed from wishlist.', 'info')
    else:
        flash('Item not found in wishlist.', 'warning')
    return redirect(url_for('wishlist'))

@app.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('product_display.html', products=products)
# ------------------ Checkout ------------------

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})

    if not cart:
        flash("Your cart is empty.", "info")
        return redirect(url_for('shop'))

    cart_items = []
    subtotal = 0
    for _, item in cart.items():
        item_total = item['price'] * item['quantity']
        cart_items.append({
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': item_total
        })
        subtotal += item_total

    # Calculate discount if coupon is applied
    discount = 0
    coupon = session.get('coupon')
    if coupon:
        if coupon['is_percentage']:
            discount = subtotal * (coupon['discount_amount'] / 100)
        else:
            discount = min(coupon['discount_amount'], subtotal)  # Don't allow negative total

    total = subtotal - discount

    # Handle EMI (Installment) payment
    emi_duration = None
    payment_method = request.form.get('payment_method')
    if payment_method == 'emi' and total > 10000:
        emi_duration = int(request.form.get('emi_duration', 3))  # Default to 3 months if not selected
        emi_amount = total / emi_duration  # EMI calculation

        # Save EMI details to database
        # Assuming you have an `emi_plans` table for storing this data
        # You may need to modify this based on your actual database setup
        # For now, I am showing just an example logic here
        new_emi_plan = EMIPlan(
            user_id=current_user.id,
            order_id=None,  # This will be set after order is placed
            total_amount=total,
            emi_duration=emi_duration,
            emi_amount=emi_amount,
            payment_method=payment_method,
            status='pending'
        )
        db.session.add(new_emi_plan)
        db.session.commit()

    return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal, discount=discount, total=total, coupon=coupon, emi_duration=emi_duration)


# ------------------ Payment Processing ------------------

@app.route('/process-payment', methods=['POST'])
@login_required
def process_payment():
    address = request.form.get('address')
    payment_method = request.form.get('payment_method')

    cart = session.get('cart', {})
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())

    # Calculate discount if coupon is applied
    discount = 0
    coupon = session.get('coupon')
    if coupon:
        if coupon['is_percentage']:
            discount = subtotal * (coupon['discount_amount'] / 100)
        else:
            discount = min(coupon['discount_amount'], subtotal)  # Don't allow negative total

    total = subtotal - discount

    if not cart:
        flash("Cart is empty.", "danger")
        return redirect(url_for('cart'))

    # Dummy order number generation (e.g., TBZ20250502XYZ)
    order_number = 'TBZ' + ''.join(random.choices(string.digits, k=6)) + ''.join(random.choices(string.ascii_uppercase, k=3))

    try:
        # Simulate payment method actions (skip Stripe)
        if payment_method == 'credit_card':
            flash("Credit Card selected. (No payment processing)", "info")
        elif payment_method == 'paypal':
            flash("Redirected to PayPal. (Simulated)", "info")
        elif payment_method == 'cash_on_delivery':
            flash("Order placed with Cash on Delivery!", "success")

        # Save order_number in session
        session['order_number'] = order_number

        # Create cart items list for database
        cart_items = []
        for _, item in cart.items():
            cart_items.append({
                'id': item['id'],
                'name': item['name'],
                'price': item['price'],
                'quantity': item['quantity']
            })

        # Create order in database
        order = Order(
            order_number=order_number,
            user_id=current_user.id,
            address=address,
            payment_method=payment_method,
            total_price=total
        )

        # Store coupon information if used
        if coupon:
            order.coupon_code = coupon['code']
            order.discount_amount = discount

        db.session.add(order)
        db.session.flush()  # Get order.id before adding items

        for item in cart_items:
            # 🔽 STOCK DEDUCTION LOGIC
            product = Product.query.get(item['id'])
            if not product or product.stock < item['quantity']:
                flash(f"Insufficient stock for {item['name']}", "danger")
                db.session.rollback()
                return redirect(url_for('cart'))
            product.stock -= item['quantity']  # Deduct stock

            order_item = OrderItem(
                order_id=order.id,
                product_id=item['id'],
                product_name=item['name'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)

        db.session.commit()

        # Clear cart and coupon
        session['cart'] = {}
        if 'coupon' in session:
            session.pop('coupon')

        return redirect(url_for('order_confirmation'))

    except Exception as e:
        db.session.rollback()
        flash(f"Error processing order: {str(e)}", "danger")
        return redirect(url_for('checkout'))


##APPLY COUPON
@app.route('/apply_coupon', methods=['POST'])
@login_required
def apply_coupon():
    coupon_code = request.form.get('coupon_code')
    if not coupon_code:
        flash("Please enter a coupon code.", 'warning')
        return redirect(url_for('cart'))

    # Find the coupon in the database
    coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()

    if not coupon:
        flash("Invalid coupon code.", 'danger')
        return redirect(url_for('cart'))

    # Store the coupon in the session
    session['coupon'] = {
        'code': coupon.code,
        'discount_amount': coupon.discount_amount,
        'is_percentage': coupon.is_percentage
    }

    # Calculate the discount amount for display
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())

    if coupon.is_percentage:
        discount = total * (coupon.discount_amount / 100)
        flash(f"Coupon applied! {coupon.discount_amount}% discount (TK {discount:.2f})", 'success')
    else:
        discount = coupon.discount_amount
        flash(f"Coupon applied! TK {discount:.2f} discount", 'success')

    return redirect(url_for('cart'))


# ------------------ App Init ------------------
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': 1
        }
    session['cart'] = cart
    flash(f"Added {product.name} to cart.", "success")
    return redirect(url_for('shop'))

@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())

    # Calculate discount if coupon is applied
    discount = 0
    coupon = session.get('coupon')
    if coupon:
        if coupon['is_percentage']:
            discount = subtotal * (coupon['discount_amount'] / 100)
        else:
            discount = min(coupon['discount_amount'], subtotal)  # Don't allow negative total

    total = subtotal - discount

    return render_template('cart.html', cart=cart, subtotal=subtotal, discount=discount, total=total, coupon=coupon)

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    cart = session.get('cart', {})
    for product_id, item in cart.items():
        new_quantity = int(request.form.get(f"quantity_{product_id}", item['quantity']))
        if new_quantity > 0:
            cart[product_id]['quantity'] = new_quantity
        else:
            del cart[product_id]
    session['cart'] = cart
    flash("Cart updated.", "info")
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    flash("Item removed from cart.", "warning")
    return redirect(url_for('cart'))

@app.route('/remove_coupon', methods=['POST'])
@login_required
def remove_coupon():
    if 'coupon' in session:
        session.pop('coupon')
        flash("Coupon removed.", "info")
    return redirect(url_for('cart'))


@app.route('/order_confirmation')
@login_required
def order_confirmation():
    order_number = session.pop('order_number', None)

    # Fetch EMI details from the session if available
    emi_duration = session.get('emi_duration', None)
    emi_amount = session.get('emi_amount', None)

    return render_template('order_confirmation.html',
        order_number=order_number,
        emi_duration=emi_duration,
        emi_amount=emi_amount)


@app.route('/return_request/<int:order_id>', methods=['GET', 'POST'])
@login_required
def create_return_request(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == 'POST':
        reason = request.form.get('reason')
        if not reason:
            flash("Please provide a reason for return.", "warning")
        else:
            return_req = ReturnRequest(order_id=order.id, user_id=current_user.id, reason=reason)
            db.session.add(return_req)
            db.session.commit()
            flash("Return request submitted.", "success")
            return redirect(url_for('order_history'))

    return render_template('return_request.html', order=order)

@app.route('/admin/returns')
@login_required
def admin_returns():
    if not current_user.is_admin:
        abort(403)
    returns = ReturnRequest.query.order_by(ReturnRequest.request_date.desc()).all()
    return render_template('admin_returns.html', returns=returns)

@app.route('/admin/returns/update/<int:return_id>/<string:action>')
@login_required
def update_return_status(return_id, action):
    if not current_user.is_admin:
        abort(403)

    return_req = ReturnRequest.query.get_or_404(return_id)
    if action == 'approve':
        return_req.status = 'Approved'
    elif action == 'reject':
        return_req.status = 'Rejected'
    elif action == 'refund':
        return_req.status = 'Refunded'
        refund = RefundStatus(return_id=return_req.id, refunded=True, refund_date=datetime.utcnow(), amount=return_req.order.total_price)
        db.session.add(refund)
    db.session.commit()
    flash(f"Return request {action}d.", "info")
    return redirect(url_for('admin_returns'))
@app.route('/returns')
@login_required
def view_returns():
    returns = ReturnRequest.query.filter_by(user_id=current_user.id).order_by(ReturnRequest.created_at.desc()).all()
    return render_template('returns_list.html', returns=returns)
@app.route('/refund-policy')
def refund_policy():
    return render_template('refund_policy.html')

@app.route('/admin/analytics')
@login_required
def analytics_dashboard():
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for('home'))

    total_sales = db.session.query(db.func.sum(OrderItem.price * OrderItem.quantity)).scalar() or 0
    total_orders = Order.query.count()

    product_performance = db.session.query(
        Product.name,
        db.func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).group_by(Product.id).order_by(db.func.sum(OrderItem.quantity).desc()).limit(10).all()

    return render_template("admin/analytics.html",
                           total_sales=total_sales,
                           total_orders=total_orders,
                           product_performance=product_performance)

# Notification Routes
@app.route('/notifications')
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=user_notifications)

@app.route('/notifications/mark_as_read/<int:notification_id>')
@login_required
def mark_notification_as_read(notification_id):
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first_or_404()
    notification.is_read = True
    db.session.commit()
    return render_template('notifications.html', notifications=get_user_notifications(current_user.id))

@app.route('/notifications/mark_all_as_read', methods=['POST'])
@login_required
def mark_all_notifications_as_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('notifications.html', notifications=get_user_notifications(current_user.id))

@app.route('/notifications/count')
@login_required
def notification_count():
    count = get_unread_notifications_count(current_user.id)
    return jsonify({'count': count})

@app.context_processor
def inject_notifications():
    if current_user.is_authenticated:
        return {
            'unread_notifications_count': get_unread_notifications_count(current_user.id),
            'recent_notifications': get_user_notifications(current_user.id, 3)
        }
    return {}


@app.template_filter('datetime')
def format_datetime(value, format="%Y-%m-%d %H:%M"):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
