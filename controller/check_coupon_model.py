from main import app, db

with app.app_context():
    # Check if there's a Coupon table
    try:
        result = db.engine.execute("SHOW TABLES LIKE 'coupon'")
        if result.rowcount > 0:
            print("Coupon table exists")
            # Check the structure of the Coupon table
            result = db.engine.execute("DESCRIBE coupon")
            print("\nCoupon table structure:")
            for row in result:
                print(f"- {row[0]}: {row[1]}")
        else:
            print("Coupon table does not exist")
    except Exception as e:
        print(f"Error checking for Coupon table: {e}")
