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
        # Get all tables that start with 'return_refunds'
        cursor.execute("SHOW TABLES LIKE 'return_refund%'")
        tables = cursor.fetchall()
        
        print(f"Found {len(tables)} tables matching 'return_refund%':")
        
        # Check each table
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get table structure
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            print(f"Columns: {len(columns)}")
            
            # Count records
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Records: {count}")
            
            # If there are records, show a sample
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                sample = cursor.fetchone()
                print(f"Sample record: {sample}")
finally:
    connection.close()
