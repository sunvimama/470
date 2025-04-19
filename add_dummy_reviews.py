from main import app, db, Review, User, Product, bcrypt
from datetime import datetime, timedelta
import random

# Sample review content templates
review_templates = [
    "This product is {adj}! I {verb} it and would {recommendation}.",
    "I've been using this for {time_period} now and it's {adj}. {recommendation}.",
    "{adj} product. {specific_comment}. {recommendation}.",
    "Bought this for my {relation} and they {reaction}. {specific_comment}. {recommendation}.",
    "The quality is {quality}. {specific_comment}. Overall, I {verb} it and would {recommendation}."
]

# Review components for generating varied content
adjectives = [
    "amazing", "excellent", "outstanding", "good", "decent", "average", "disappointing",
    "terrible", "fantastic", "superb", "mediocre", "subpar", "exceptional"
]

verbs = [
    "love", "like", "enjoy", "hate", "dislike", "adore", "appreciate", "can't stand",
    "am impressed by", "am disappointed with", "am satisfied with"
]

recommendations = [
    "definitely recommend it", "recommend it to everyone", "not recommend it",
    "suggest looking at alternatives", "buy it again", "recommend it with some reservations",
    "highly recommend it", "only recommend it if on sale"
]

time_periods = [
    "a week", "a month", "two weeks", "three months", "six months", "a year", "a few days"
]

specific_comments = [
    "The design is sleek and modern", "It works exactly as described",
    "The battery life is impressive", "Setup was a breeze", "Customer service was helpful",
    "Shipping was fast", "The price is a bit high for what you get",
    "It's not as durable as I expected", "The interface is intuitive",
    "It's missing some key features", "The performance exceeds expectations",
    "It's perfect for everyday use", "The build quality could be better"
]

relations = [
    "mom", "dad", "sister", "brother", "friend", "partner", "spouse", "grandparent", "child"
]

reactions = [
    "loved it", "was impressed", "was disappointed", "found it useful",
    "couldn't figure out how to use it", "uses it every day", "returned it"
]

quality_levels = [
    "top-notch", "excellent", "good", "decent", "average", "below average", "poor"
]

def generate_review_content():
    template = random.choice(review_templates)

    # Replace placeholders with random choices
    content = template.format(
        adj=random.choice(adjectives),
        verb=random.choice(verbs),
        recommendation=random.choice(recommendations),
        time_period=random.choice(time_periods),
        specific_comment=random.choice(specific_comments),
        relation=random.choice(relations),
        reaction=random.choice(reactions),
        quality=random.choice(quality_levels)
    )

    return content

def create_dummy_reviews(num_reviews=15):
    with app.app_context():
        # Get all users and products
        users = User.query.all()
        products = Product.query.all()

        if not users:
            print("No users found in the database. Please create users first.")
            return

        if not products:
            print("No products found in the database. Please create products first.")
            return

        print(f"Found {len(users)} users and {len(products)} products")

        # Generate random reviews
        reviews_added = 0
        for _ in range(num_reviews):
            user = random.choice(users)
            product = random.choice(products)

            # Check if this user has already reviewed this product
            existing_review = Review.query.filter_by(
                user_id=user.id,
                product_id=product.id
            ).first()

            if existing_review:
                continue  # Skip if user already reviewed this product

            # Generate random rating (1-5)
            rating = random.randint(1, 5)

            # Generate review content
            content = generate_review_content()

            # Generate random timestamp within the last 30 days
            days_ago = random.randint(0, 30)
            timestamp = datetime.now() - timedelta(days=days_ago)

            # Create new review
            new_review = Review(
                content=content,
                rating=rating,
                user_id=user.id,
                product_id=product.id,
                timestamp=timestamp
            )

            db.session.add(new_review)
            reviews_added += 1

        try:
            db.session.commit()
            print(f"Successfully added {reviews_added} dummy reviews to the database!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding reviews: {str(e)}")

def create_dummy_users(num_users=5):
    """Create dummy users for testing"""
    with app.app_context():
        users_created = 0

        # Sample user data
        first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Lisa", "William", "Emma"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]

        for i in range(num_users):
            # Generate unique user data
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            email = f"user{i+1}@example.com"
            nid = 1000000 + i
            phone = 1000000000 + i

            # Check if user with this email already exists
            existing_user = User.query.filter_by(Email=email).first()
            if existing_user:
                continue

            try:
                new_user = User(
                    Name=name,
                    Email=email,
                    Nid=nid,
                    phone=phone,
                    is_admin=False,
                    password=bcrypt.generate_password_hash("password123").decode('utf-8')
                )
                db.session.add(new_user)
                users_created += 1
            except Exception as e:
                print(f"Error creating user {email}: {str(e)}")
                continue

        try:
            db.session.commit()
            print(f"Successfully created {users_created} new users")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing users: {str(e)}")

if __name__ == "__main__":
    # Create dummy users first
    create_dummy_users(5)

    # Create dummy reviews
    create_dummy_reviews(30)  # Create 30 dummy reviews
