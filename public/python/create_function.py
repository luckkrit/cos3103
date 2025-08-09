import pymysql

# Connect to MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='aod_company'
)

cursor = connection.cursor()

# Create function using SQL
function_sql = """
DROP FUNCTION IF EXISTS giveRaise2;
"""

cursor.execute(function_sql)

function_sql2 = """
CREATE FUNCTION giveRaise2(oldval DECIMAL(10,2), amount DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE newval DECIMAL(10,2);
    SET newval = oldval * (1 + amount);
    RETURN newval;
END
"""

cursor.execute(function_sql2)
connection.commit()

# Use the function in queries
cursor.execute("SELECT name, salary, giveRaise2(salary, 0.10) AS new_salary FROM employee")
results = cursor.fetchall()

for row in results:
    print(f"Employee: {row[0]}, Current: {row[1]}, New: {row[2]}")

# Don't forget to close
cursor.close()
connection.close()