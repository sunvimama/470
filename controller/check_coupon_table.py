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
        # Check the structure of the coupon table
        cursor.execute("DESCRIBE coupon")
        columns = cursor.fetchall()
        print("Columns in coupon table:")
        for column in columns:
            print(f"- {column[0]}: {column[1]}")
        
        # Check existing coupons
        cursor.execute("SELECT * FROM coupon")
        coupons = cursor.fetchall()
        print("\nExisting coupons:")
        for coupon in coupons:
            print(f"- ID: {coupon[0]}, Code: {coupon[1]}, Discount: {coupon[2]}, Is Percentage: {coupon[3]}, Active: {coupon[6]}")
finally:
    connection.close()
