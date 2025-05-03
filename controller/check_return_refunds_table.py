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
        # Check if return_refunds table exists
        cursor.execute("SHOW TABLES LIKE 'return_refunds'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            print("return_refunds table exists!")
            # Get the structure of the table
            cursor.execute("DESCRIBE return_refunds")
            columns = cursor.fetchall()
            print("\nColumns in return_refunds table:")
            for column in columns:
                print(f"- {column[0]}: {column[1]}, Nullable: {column[2]}, Key: {column[3]}, Default: {column[4]}")
                
            # Check if there's any data in the table
            cursor.execute("SELECT COUNT(*) FROM return_refunds")
            count = cursor.fetchone()[0]
            print(f"\nNumber of records in return_refunds table: {count}")
        else:
            print("return_refunds table does not exist!")
finally:
    connection.close()
