import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='aod_company'
    )
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT checkAge(16);")
    
    
except pymysql.Error as e:
    print(f"Error: {e}")
    
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()