from main import app, db

def create_coupon_table():
    """Create the coupon table in the database"""
    with app.app_context():
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        
        # Check if coupon table exists
        cursor.execute("SHOW TABLES LIKE 'coupon'")
        coupon_exists = cursor.fetchone() is not None
        
        if not coupon_exists:
            print("Creating coupon table...")
            cursor.execute("""
            CREATE TABLE coupon (
                id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(50) UNIQUE NOT NULL,
                discount_amount FLOAT NOT NULL,
                is_percentage BOOLEAN DEFAULT FALSE,
                valid_from DATETIME,
                valid_to DATETIME,
                is_active BOOLEAN DEFAULT TRUE
            )
            """)
            
            # Add some sample coupons
            cursor.execute("""
            INSERT INTO coupon (code, discount_amount, is_percentage, is_active)
            VALUES 
                ('WELCOME10', 10, TRUE, TRUE),
                ('SAVE20', 20, TRUE, TRUE),
                ('FLAT50', 50, FALSE, TRUE)
            """)
            
            connection.commit()
            print("Coupon table created successfully with sample coupons!")
        else:
            print("Coupon table already exists.")
            
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_coupon_table()
