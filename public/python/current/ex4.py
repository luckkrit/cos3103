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

print(results[0]) # row 0

for row in results: # print all rows
    for key, value in row.items():
        print(f"Key = {key}, Value = {value}\n")


cursor.close()
connection.close()