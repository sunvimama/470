import pymysql
import random
from datetime import datetime, timedelta

# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='etech'
)

try:
    with connection.cursor() as cursor:
        # Check if return_refunds table exists
        cursor.execute("SHOW TABLES LIKE 'return_refunds'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            print("Creating return_refunds table...")
            # Create the return_refunds table
            cursor.execute("""
            CREATE TABLE return_refunds (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                reason TEXT NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'Pending',
                request_date DATETIME NOT NULL,
                processed_date DATETIME,
                refund_amount FLOAT,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (product_id) REFERENCES product(id)
            )
            """)
            print("return_refunds table created successfully!")
        
        # Get some order IDs, user IDs, and product IDs for the dummy data
        cursor.execute("SELECT id FROM orders LIMIT 10")
        order_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM user LIMIT 10")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM product LIMIT 10")
        product_ids = [row[0] for row in cursor.fetchall()]
        
        # If we have orders, users, and products, add dummy data
        if order_ids and user_ids and product_ids:
            print("Adding dummy data to return_refunds table...")
            
            # Sample reasons for returns/refunds
            reasons = [
                "Product arrived damaged",
                "Wrong item received",
                "Product not as described",
                "Changed my mind",
                "Found a better price elsewhere",
                "Product is defective",
                "Missing parts or accessories",
                "Ordered by mistake",
                "Arrived too late",
                "Quality not as expected"
            ]
            
            # Sample statuses
            statuses = ["Pending", "Approved", "Rejected", "Processing", "Completed"]
            
            # Generate 10 dummy records
            for i in range(10):
                # Randomly select order, user, and product IDs
                order_id = random.choice(order_ids) if order_ids else 1
                user_id = random.choice(user_ids) if user_ids else 1
                product_id = random.choice(product_ids) if product_ids else 1
                
                # Randomly select a reason
                reason = random.choice(reasons)
                
                # Randomly select a status
                status = random.choice(statuses)
                
                # Generate random dates
                request_date = datetime.now() - timedelta(days=random.randint(1, 30))
                processed_date = request_date + timedelta(days=random.randint(1, 7)) if status != "Pending" else None
                
                # Generate random refund amount
                refund_amount = round(random.uniform(50, 500), 2) if status in ["Approved", "Completed"] else None
                
                # Insert the record
                cursor.execute("""
                INSERT INTO return_refunds 
                (order_id, user_id, product_id, reason, status, request_date, processed_date, refund_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    order_id, 
                    user_id, 
                    product_id, 
                    reason, 
                    status, 
                    request_date, 
                    processed_date, 
                    refund_amount
                ))
            
            # Commit the changes
            connection.commit()
            print("10 dummy records added to return_refunds table!")
            
            # Verify the data was added
            cursor.execute("SELECT * FROM return_refunds")
            records = cursor.fetchall()
            print(f"\nTotal records in return_refunds table: {len(records)}")
            print("\nSample records:")
            for i, record in enumerate(records[:3]):  # Show first 3 records
                print(f"Record {i+1}: {record}")
        else:
            print("Could not add dummy data: No orders, users, or products found in the database.")
            
except Exception as e:
    print(f"Error: {e}")
    connection.rollback()
finally:
    connection.close()
