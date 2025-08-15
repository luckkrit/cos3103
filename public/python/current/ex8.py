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

users_data = [
            ('John Smith', 'john.smith@email.com'),
            ('Sarah Johnson', 'sarah.johnson@email.com'),
            ('Mike Davis', 'mike.davis@email.com'),
            ('Emily Brown', 'emily.brown@email.com'),
            ('David Wilson', 'david.wilson@email.com')
        ]
        
sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
        
for name, email in users_data:
    cursor.execute(sql, (name, email))
            
cursor.close()
connection.commit()
connection.close() 