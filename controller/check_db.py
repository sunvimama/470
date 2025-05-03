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
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
            
            # Get the structure of each table
            cursor.execute(f"DESCRIBE {table[0]}")
            columns = cursor.fetchall()
            print(f"  Columns in {table[0]}:")
            for column in columns:
                print(f"  - {column[0]}: {column[1]}")
            print()
finally:
    connection.close()
