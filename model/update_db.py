from main import app, db
import pymysql

def update_orders_table():
    """Update the orders table to match the new model"""
    with app.app_context():
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        
        # Check if order_number column exists
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'order_number'")
        order_number_exists = cursor.fetchone() is not None
        
        # Check if total_price column exists
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'total_price'")
        total_price_exists = cursor.fetchone() is not None
        
        # Check if address column exists
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'address'")
        address_exists = cursor.fetchone() is not None
        
        # Check if payment_method column exists
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'payment_method'")
        payment_method_exists = cursor.fetchone() is not None
        
        # Add missing columns
        try:
            if not order_number_exists:
                print("Adding order_number column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN order_number VARCHAR(20) UNIQUE")
            
            if not total_price_exists:
                print("Adding total_price column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN total_price FLOAT NOT NULL DEFAULT 0")
            
            if not address_exists:
                print("Adding address column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN address VARCHAR(200) NOT NULL DEFAULT ''")
            
            if not payment_method_exists:
                print("Adding payment_method column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50) NOT NULL DEFAULT 'cash_on_delivery'")
            
            # Check if product_id and quantity columns exist and should be removed
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'product_id'")
            product_id_exists = cursor.fetchone() is not None
            
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'quantity'")
            quantity_exists = cursor.fetchone() is not None
            
            # Create order_items table if it doesn't exist
            cursor.execute("SHOW TABLES LIKE 'order_items'")
            order_items_exists = cursor.fetchone() is not None
            
            if not order_items_exists:
                print("Creating order_items table...")
                cursor.execute("""
                CREATE TABLE order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT NOT NULL,
                    product_id INT NOT NULL,
                    product_name VARCHAR(100) NOT NULL,
                    quantity INT NOT NULL,
                    price FLOAT NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES product(id)
                )
                """)
            
            connection.commit()
            print("Database schema updated successfully!")
            
        except Exception as e:
            connection.rollback()
            print(f"Error updating database schema: {e}")
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    update_orders_table()
