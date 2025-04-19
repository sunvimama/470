from main import app, db, Review, User, Product
from sqlalchemy import func

with app.app_context():
    # Get total number of reviews
    total_reviews = Review.query.count()
    print(f"Total reviews: {total_reviews}")

    # Get average rating
    avg_rating = db.session.query(func.avg(Review.rating)).scalar()
    print(f"Average rating: {avg_rating:.2f}/5")

    # Get rating distribution
    rating_counts = db.session.query(Review.rating, func.count(Review.id)).group_by(Review.rating).all()
    print("\nRating distribution:")
    for rating, count in rating_counts:
        percentage = (count / total_reviews) * 100
        print(f"{rating} stars: {count} reviews ({percentage:.1f}%)")

    # Get product statistics
    print("\nProduct statistics:")
    product_stats = db.session.query(
        Product.id,
        Product.name,
        func.count(Review.id).label('review_count'),
        func.avg(Review.rating).label('avg_rating')
    ).join(Review, Product.id == Review.product_id).group_by(Product.id).all()

    for product_id, name, review_count, avg_rating in product_stats:
        print(f"{name}: {review_count} reviews, average rating: {avg_rating:.2f}/5")

    # Get user statistics
    print("\nTop reviewers:")
    user_stats = db.session.query(
        User.id,
        User.Name,
        func.count(Review.id).label('review_count')
    ).join(Review, User.id == Review.user_id).group_by(User.id).order_by(func.count(Review.id).desc()).limit(5).all()

    for user_id, name, review_count in user_stats:
        print(f"{name}: {review_count} reviews")
