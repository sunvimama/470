from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from functools import wraps
import random
import string
import stripe

load_dotenv()

app = Flask(__name__)
app.secret_key = "sunvi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/etech'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------ Models ------------------

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

    if request.method == 'POST':
        new_status = request.form.get('status')
        if new_status:
            order.status = new_status
            db.session.commit()
            flash(f"Order status updated to {new_status}.", "success")
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
            product = Product(
                name=request.form['name'],
                description=request.form['description'],
                price=float(request.form['price']),
                stock=int(request.form['stock']),
                image_url=request.form['image_url']
            )
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
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
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = float(request.form['price'])
            product.stock = int(request.form['stock'])
            product.image_url = request.form['image_url']
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
    existing_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not existing_item:
        new_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(new_item)
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

    return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal, discount=discount, total=total, coupon=coupon)

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
        if payment_method == 'credit_card':
            # Simulated Stripe charge
            stripe.api_key = "your_stripe_test_key"  # You should use environment variables for this
            stripe.PaymentIntent.create(
                amount=int(total * 100),  # convert dollars to cents
                currency='usd',
                payment_method_types=['card'],
                metadata={'order_id': order_number}
            )
            flash("Payment successful! (Stripe simulation)", "success")
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

    except stripe.error.StripeError as e:
        flash(f"Payment failed: {e.user_message}", "danger")
        return redirect(url_for('checkout'))
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
    return render_template('order_confirmation.html', order_number=order_number)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
