import pymysql
connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    database='classicmodels',
    cursorclass=pymysql.cursors.DictCursor  # Return dictionary of row that access by column name
)
print(connection)