import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='aod_company'
    )
    
    cursor = connection.cursor()
    
    # Create procedure
    cursor.execute("DROP PROCEDURE IF EXISTS giveRaise")
    
    procedure_sql = """
    CREATE PROCEDURE giveRaise(IN amount DOUBLE)
    BEGIN
        UPDATE employee 
        SET salary = salary + ROUND(salary * amount)
        WHERE salary IS NOT NULL;
    END
    """
    
    cursor.execute(procedure_sql)
    connection.commit()
    
    print("Stored procedure created successfully!")
    
    # Test the procedure
    cursor.execute("CALL giveRaise(0.05)")  # 5% raise
    connection.commit()
    
    print("Procedure executed successfully!")


    # Use the function in queries
    cursor.execute("SELECT name, salary, giveRaise2(salary, 0.10) AS new_salary FROM employee")
    results = cursor.fetchall()

    for row in results:
        print(f"Employee: {row[0]}, Current: {row[1]}, New: {row[2]}")
    
except pymysql.Error as e:
    print(f"Error: {e}")
    
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()