import pymysql

def create_employee_triggers():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='aod_company'
        )
        
        cursor = connection.cursor()
        
        # Create INSERT trigger
        cursor.execute("DROP TRIGGER IF EXISTS update_salary")
        
        insert_trigger = """
        CREATE TRIGGER update_salary
        AFTER INSERT ON employee
        FOR EACH ROW
        BEGIN
            IF NEW.dno IS NOT NULL THEN
                UPDATE deptsal
                SET totalsalary = totalsalary + NEW.salary
                WHERE dnumber = NEW.dno;
            END IF;
        END
        """
        
        cursor.execute(insert_trigger)
        
        # Create UPDATE trigger
        cursor.execute("DROP TRIGGER IF EXISTS update_salary2")
        
        update_trigger = """
        CREATE TRIGGER update_salary2
        AFTER UPDATE ON employee
        FOR EACH ROW
        BEGIN
            IF OLD.dno IS NOT NULL THEN
                UPDATE deptsal
                SET totalsalary = totalsalary - OLD.salary
                WHERE dnumber = OLD.dno;
            END IF;
            IF NEW.dno IS NOT NULL THEN
                UPDATE deptsal
                SET totalsalary = totalsalary + NEW.salary
                WHERE dnumber = NEW.dno;
            END IF;
        END
        """
        
        cursor.execute(update_trigger)
        
        # Create DELETE trigger
        cursor.execute("DROP TRIGGER IF EXISTS update_salary3")
        
        delete_trigger = """
        CREATE TRIGGER update_salary3
        BEFORE DELETE ON employee
        FOR EACH ROW
        BEGIN
            IF OLD.dno IS NOT NULL THEN
                UPDATE deptsal
                SET totalsalary = totalsalary - OLD.salary
                WHERE dnumber = OLD.dno;
            END IF;
        END
        """
        
        cursor.execute(delete_trigger)
        
        connection.commit()
        print("All triggers created successfully!")
        
        # Show created triggers
        cursor.execute("SHOW TRIGGERS")
        triggers = cursor.fetchall()
        print("\nCreated triggers:")
        for trigger in triggers:
            print(f"- {trigger[0]} on {trigger[1]}")
            
    except pymysql.Error as e:
        print(f"Error creating triggers: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Run the function
create_employee_triggers()