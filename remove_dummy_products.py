from main import app, db, Product, Review, OrderItem, Wishlist

# IDs of dummy products to remove
dummy_product_ids = [1, 2, 3]

with app.app_context():
    try:
        # Get the products to be removed
        products_to_remove = Product.query.filter(Product.id.in_(dummy_product_ids)).all()

        if products_to_remove:
            print(f"Found {len(products_to_remove)} dummy products to remove:")
            for product in products_to_remove:
                print(f"ID: {product.id}, Name: {product.name}, Price: {product.price}")

            # First, delete all associated reviews
            for product_id in dummy_product_ids:
                reviews = Review.query.filter_by(product_id=product_id).all()
                if reviews:
                    print(f"Deleting {len(reviews)} reviews for product ID {product_id}")
                    for review in reviews:
                        db.session.delete(review)

            # Delete any order items associated with these products
            for product_id in dummy_product_ids:
                order_items = OrderItem.query.filter_by(product_id=product_id).all()
                if order_items:
                    print(f"Deleting {len(order_items)} order items for product ID {product_id}")
                    for item in order_items:
                        db.session.delete(item)

            # Delete any wishlist items associated with these products
            for product_id in dummy_product_ids:
                wishlist_items = Wishlist.query.filter_by(product_id=product_id).all()
                if wishlist_items:
                    print(f"Deleting {len(wishlist_items)} wishlist items for product ID {product_id}")
                    for item in wishlist_items:
                        db.session.delete(item)

            # Now delete the products
            for product in products_to_remove:
                db.session.delete(product)

            # Commit the changes
            db.session.commit()
            print("\nDummy products and their associated data successfully removed!")
        else:
            print("No dummy products found with the specified IDs.")

        # Check remaining products
        remaining_products = Product.query.all()
        print(f"\nRemaining products ({len(remaining_products)}):")
        for product in remaining_products:
            print(f"ID: {product.id}, Name: {product.name}, Price: {product.price}")

    except Exception as e:
        db.session.rollback()
        print(f"Error removing dummy products: {str(e)}")
