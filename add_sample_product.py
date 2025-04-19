from main import app, Product, db

with app.app_context():
    # Check if the product already exists
    existing_product = Product.query.filter_by(name="Sample Smartphone").first()
    
    if not existing_product:
        # Create a sample product
        sample_product = Product(
            name="Sample Smartphone",
            description="A high-end smartphone with advanced features",
            price=599.99,
            stock=10,
            image_url="https://via.placeholder.com/300x200"
        )
        
        # Add to database
        db.session.add(sample_product)
        db.session.commit()
        print("Sample product added successfully!")
    else:
        print("Sample product already exists.")
