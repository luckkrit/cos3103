import pymysql
connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    database='shop_db',
    cursorclass=pymysql.cursors.DictCursor  # Return dictionary of row that access by column name
)
cursor = connection.cursor()

        
sql = "UPDATE users SET name = %s WHERE id = %s"
name = "Krit Chomaitong" 
cursor.execute(sql, (name, 5))
            
cursor.close()
connection.commit() # Commit to save changes
connection.close() 