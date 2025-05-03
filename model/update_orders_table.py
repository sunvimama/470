from main import app, db

def update_orders_table():
    """Update the orders table to add coupon fields"""
    with app.app_context():
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        
        # Check if coupon_code column exists
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'coupon_code'")
        coupon_code_exists = cursor.fetchone() is not None
        
        # Check if discount_amount column exists
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'discount_amount'")
        discount_amount_exists = cursor.fetchone() is not None
        
        # Add missing columns
        try:
            if not coupon_code_exists:
                print("Adding coupon_code column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN coupon_code VARCHAR(50)")
            
            if not discount_amount_exists:
                print("Adding discount_amount column to orders table...")
                cursor.execute("ALTER TABLE orders ADD COLUMN discount_amount FLOAT")
            
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
