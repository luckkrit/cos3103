import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='aod_company'
)

cursor = connection.cursor()

# Test INSERT trigger
print("Testing INSERT trigger...")
cursor.execute("INSERT INTO employee VALUES (8, 'alice', NULL, 60000, '1990-05-15', 2)")
connection.commit()

# Check deptsal table
cursor.execute("SELECT * FROM deptsal WHERE dnumber = 2")
results = cursor.fetchall()

for row in results:
    print(f"Dept: {row[0]}, Total Salary: {row[1]}")

cursor.close()
connection.close()