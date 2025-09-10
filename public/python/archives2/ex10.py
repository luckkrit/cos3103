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

        
sql = "DELETE FROM users WHERE id = %s"
cursor.execute(sql, ( 5))
            
cursor.close()
connection.commit() # Commit to save changes
connection.close() 