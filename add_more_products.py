from main import app, Product, db

with app.app_context():
    # Add a second product
    product2 = Product.query.filter_by(name="Wireless Headphones").first()
    if not product2:
        product2 = Product(
            name="Wireless Headphones",
            description="Noise-cancelling wireless headphones with 30-hour battery life",
            price=199.99,
            stock=15,
            image_url="https://via.placeholder.com/300x200"
        )
        db.session.add(product2)
        
    # Add a third product
    product3 = Product.query.filter_by(name="Ultra HD Smart TV").first()
    if not product3:
        product3 = Product(
            name="Ultra HD Smart TV",
            description="55-inch 4K Ultra HD Smart TV with HDR",
            price=899.99,
            stock=5,
            image_url="https://via.placeholder.com/300x200"
        )
        db.session.add(product3)
    
    db.session.commit()
    print("Additional products added successfully!")
