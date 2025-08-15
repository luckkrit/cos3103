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
cursor.execute('select * from customers where creditLimit between %s and %s', [100000, 110000])
results = cursor.fetchall()

for row in results: # print all rows
    print(row['creditLimit'])


cursor.close()
connection.close()