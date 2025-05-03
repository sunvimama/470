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
        # Check the structure of the orders table
        cursor.execute("DESCRIBE orders")
        columns = cursor.fetchall()
        print("Columns in orders table:")
        for column in columns:
            print(f"- {column[0]}: {column[1]}, Nullable: {column[2]}, Key: {column[3]}, Default: {column[4]}")
finally:
    connection.close()
