from main import app, Review, User, Product

with app.app_context():
    reviews = Review.query.all()
    
    if reviews:
        print(f"Found {len(reviews)} reviews in the database:")
        print("-" * 80)
        
        for review in reviews:
            user = User.query.get(review.user_id)
            product = Product.query.get(review.product_id)
            
            print(f"Review ID: {review.id}")
            print(f"Product: {product.name} (ID: {product.id})")
            print(f"User: {user.Name} (ID: {user.id})")
            print(f"Rating: {review.rating}/5")
            print(f"Date: {review.timestamp}")
            print(f"Content: {review.content}")
            print("-" * 80)
    else:
        print("No reviews found in the database.")
