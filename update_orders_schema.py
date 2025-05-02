from main import app, db

def update_orders_table():
    """Update the orders table to match the new model"""
    with app.app_context():
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        
        try:
            # Check if order_number column exists
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'order_number'")
            order_number_exists = cursor.fetchone() is not None
            
            # Check if address column exists
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'address'")
            address_exists = cursor.fetchone() is not None
            
            # Check if payment_method column exists
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'payment_method'")
            payment_method_exists = cursor.fetchone() is not None
            
            # Check if total_price column exists
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'total_price'")
            total_price_exists = cursor.fetchone() is not None
            
            # Add missing columns
            if not order_number_exists:
                print("Adding order_number column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN order_number VARCHAR(20) UNIQUE")
            
            if not address_exists:
                print("Adding address column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN address VARCHAR(200) NOT NULL DEFAULT ''")
            
            if not payment_method_exists:
                print("Adding payment_method column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50) NOT NULL DEFAULT 'cash_on_delivery'")
            
            if not total_price_exists:
                print("Adding total_price column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN total_price FLOAT NOT NULL DEFAULT 0")
            
            # Make product_id and quantity nullable (since they're not in the new model)
            cursor.execute("ALTER TABLE orders MODIFY COLUMN product_id INT NULL")
            cursor.execute("ALTER TABLE orders MODIFY COLUMN quantity INT NULL")
            
            connection.commit()
            print("Orders table updated successfully!")
            
        except Exception as e:
            connection.rollback()
            print(f"Error updating orders table: {e}")
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    update_orders_table()
