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
        # Check if the table exists
        cursor.execute("SHOW TABLES LIKE 'returns_refunds'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            # Drop the empty table
            print("Dropping empty 'returns_refunds' table...")
            cursor.execute("DROP TABLE returns_refunds")
            connection.commit()
            print("Table 'returns_refunds' has been dropped successfully!")
        else:
            print("Table 'returns_refunds' does not exist.")
            
        # Verify the remaining return_refunds table
        cursor.execute("SHOW TABLES LIKE 'return_refund%'")
        tables = cursor.fetchall()
        print(f"\nRemaining tables matching 'return_refund%': {len(tables)}")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Table: {table_name}, Records: {count}")
except Exception as e:
    print(f"Error: {e}")
    connection.rollback()
finally:
    connection.close()
