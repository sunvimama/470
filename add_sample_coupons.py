import pymysql

# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='etech'
)

try:
    with connection.cursor() as cursor:
        # Add sample coupons
        cursor.execute("""
        INSERT INTO coupon (code, discount_amount, is_percentage, is_active)
        VALUES 
            ('WELCOME10', 10, TRUE, TRUE),
            ('SAVE20', 20, TRUE, TRUE),
            ('FLAT50', 50, FALSE, TRUE)
        """)
        
        connection.commit()
        print("Sample coupons added successfully!")
        
        # Verify the coupons were added
        cursor.execute("SELECT * FROM coupon")
        coupons = cursor.fetchall()
        print("\nCoupons in database:")
        for coupon in coupons:
            print(f"- ID: {coupon[0]}, Code: {coupon[1]}, Discount: {coupon[2]}, Is Percentage: {coupon[3]}, Active: {coupon[6]}")
finally:
    connection.close()
