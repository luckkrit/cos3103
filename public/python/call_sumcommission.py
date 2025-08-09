import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='aco_db'
)

with connection.cursor() as cursor:
    # Call sumCommission - it only SELECTs data
    cursor.callproc('sumCommission', (0.1, 0.4))
    
    # Get first result set (sumCOMMISSIONV, agent_code_L)
    result1 = cursor.fetchone()
    print("Total and codes:", result1)
    
    # Get second result set (AGENT_NAME_L, COMMISSION_L)
    if cursor.nextset():
        result2 = cursor.fetchone()
        print("Names and commissions:", result2)
    

connection.close()