from main import app, Product, db

with app.app_context():
    products = Product.query.all()
    if products:
        print(f"Found {len(products)} products:")
        for product in products:
            print(f"ID: {product.id}, Name: {product.name}, Price: {product.price}, Stock: {product.stock}")
    else:
        print("No products found in the database.")
