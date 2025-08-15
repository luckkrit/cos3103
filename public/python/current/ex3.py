import pymysql
connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    database='classicmodels',
    cursorclass=pymysql.cursors.DictCursor  # Return dictionary of row that access by column name
)

cursor = connection.cursor()
cursor.execute('select * from customers')
results = cursor.fetchall()

for key, value in results[0].items():
    print(f"Key = {key}, Value = {value}")


cursor.close()
connection.close()