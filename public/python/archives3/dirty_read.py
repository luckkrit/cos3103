import pymysql
import threading
import time
from contextlib import contextmanager

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'test_db',
    'charset': 'utf8mb4'
}

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        yield connection
    finally:
        connection.close()

def setup_database():
    """Setup test tables"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create accounts table for examples
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INT PRIMARY KEY,
            name VARCHAR(50),
            balance DECIMAL(10,2)
        )
        """)
        
        # Create products table for phantom read example
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50),
            price DECIMAL(10,2)
        )
        """)
        
        # Insert sample data
        cursor.execute("DELETE FROM accounts")
        cursor.execute("DELETE FROM products")
        
        cursor.execute("INSERT INTO accounts VALUES (1, 'Alice', 1000.00)")
        cursor.execute("INSERT INTO accounts VALUES (2, 'Bob', 1500.00)")
        
        cursor.execute("INSERT INTO products (category, price) VALUES ('Electronics', 100.00)")
        cursor.execute("INSERT INTO products (category, price) VALUES ('Electronics', 200.00)")
        
        conn.commit()

# =============================================================================
# 1. LOST UPDATE PROBLEM (Write-Write Conflict)
# =============================================================================

def lost_update_demo():
    """Demonstrates the lost update problem"""
    print("=== LOST UPDATE PROBLEM DEMO ===")
    
    def transaction1():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            print("T1: Reading Alice's balance...")
            cursor.execute("SELECT balance FROM accounts WHERE id = 1")
            balance = cursor.fetchone()[0]
            print(f"T1: Alice's balance is {balance}")
            
            # Simulate processing time
            time.sleep(2)
            
            new_balance = balance + 100  # Add $100
            print(f"T1: Updating Alice's balance to {new_balance}")
            cursor.execute("UPDATE accounts SET balance = %s WHERE id = 1", (new_balance,))
            conn.commit()
            print("T1: Transaction committed")
    
    def transaction2():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            time.sleep(1)  # Start slightly after T1
            
            print("T2: Reading Alice's balance...")
            cursor.execute("SELECT balance FROM accounts WHERE id = 1")
            balance = cursor.fetchone()[0]
            print(f"T2: Alice's balance is {balance}")
            
            # Simulate processing time
            time.sleep(1)
            
            new_balance = balance + 50  # Add $50
            print(f"T2: Updating Alice's balance to {new_balance}")
            cursor.execute("UPDATE accounts SET balance = %s WHERE id = 1", (new_balance,))
            conn.commit()
            print("T2: Transaction committed")
    
    # Reset Alice's balance
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = 1000.00 WHERE id = 1")
        conn.commit()
    
    # Run transactions concurrently
    t1 = threading.Thread(target=transaction1)
    t2 = threading.Thread(target=transaction2)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    # Check final balance
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = 1")
        final_balance = cursor.fetchone()[0]
        print(f"Final balance: {final_balance} (Expected: 1150, but one update is lost!)")

# =============================================================================
# 2. DIRTY READ PROBLEM (Write-Read Conflict)
# =============================================================================

def dirty_read_demo():
    """Demonstrates the dirty read problem"""
    print("\n=== DIRTY READ PROBLEM DEMO ===")
    
    def transaction1():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            print("T1: Starting transaction...")
            conn.begin()
            
            print("T1: Updating Bob's balance...")
            cursor.execute("UPDATE accounts SET balance = balance + 500 WHERE id = 2")
            
            # Simulate processing time before rollback
            time.sleep(3)
            
            print("T1: Rolling back transaction...")
            conn.rollback()
            print("T1: Transaction rolled back")
    
    def transaction2():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            time.sleep(1)  # Start after T1 has updated
            
            print("T2: Reading Bob's balance...")
            cursor.execute("SELECT balance FROM accounts WHERE id = 2")
            balance = cursor.fetchone()[0]
            print(f"T2: Bob's balance is {balance} (This is a dirty read!)")
            
            # Use this dirty data for further processing
            if balance > 1800:
                print("T2: Balance is high enough, proceeding with loan approval...")
    
    # Reset Bob's balance
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = 1500.00 WHERE id = 2")
        conn.commit()
    
    t1 = threading.Thread(target=transaction1)
    t2 = threading.Thread(target=transaction2)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

# =============================================================================
# 3. INCORRECT SUMMARY PROBLEM
# =============================================================================

def incorrect_summary_demo():
    """Demonstrates the incorrect summary problem"""
    print("\n=== INCORRECT SUMMARY PROBLEM DEMO ===")
    
    def transaction1():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            print("T1: Starting money transfer...")
            
            # Transfer $200 from Alice to Bob
            cursor.execute("UPDATE accounts SET balance = balance - 200 WHERE id = 1")
            print("T1: Deducted $200 from Alice")
            
            # Simulate processing time
            time.sleep(2)
            
            cursor.execute("UPDATE accounts SET balance = balance + 200 WHERE id = 2")
            print("T1: Added $200 to Bob")
            
            conn.commit()
            print("T1: Transfer completed")
    
    def transaction2():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            time.sleep(1)  # Start during T1's execution
            
            print("T2: Calculating total balance...")
            
            # Read Alice's balance (after deduction)
            cursor.execute("SELECT balance FROM accounts WHERE id = 1")
            alice_balance = cursor.fetchone()[0]
            print(f"T2: Alice's balance: {alice_balance}")
            
            # Read Bob's balance (before addition)
            cursor.execute("SELECT balance FROM accounts WHERE id = 2")
            bob_balance = cursor.fetchone()[0]
            print(f"T2: Bob's balance: {bob_balance}")
            
            total = alice_balance + bob_balance
            print(f"T2: Total balance: {total} (Incorrect! Money appears to be lost)")
    
    # Reset balances
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = 1000.00 WHERE id = 1")
        cursor.execute("UPDATE accounts SET balance = 1500.00 WHERE id = 2")
        conn.commit()
    
    t1 = threading.Thread(target=transaction1)
    t2 = threading.Thread(target=transaction2)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

# =============================================================================
# 4. NONREPEATABLE READ PROBLEM
# =============================================================================

def nonrepeatable_read_demo():
    """Demonstrates the nonrepeatable read problem"""
    print("\n=== NONREPEATABLE READ PROBLEM DEMO ===")
    
    def transaction1():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            print("T1: First read of Alice's balance...")
            cursor.execute("SELECT balance FROM accounts WHERE id = 1")
            balance1 = cursor.fetchone()[0]
            print(f"T1: First read - Alice's balance: {balance1}")
            
            # Simulate some processing time
            time.sleep(3)
            
            print("T1: Second read of Alice's balance...")
            cursor.execute("SELECT balance FROM accounts WHERE id = 1")
            balance2 = cursor.fetchone()[0]
            print(f"T1: Second read - Alice's balance: {balance2}")
            
            if balance1 != balance2:
                print("T1: NONREPEATABLE READ! Balance changed between reads")
    
    def transaction2():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            time.sleep(1)  # Start after T1's first read
            
            print("T2: Updating Alice's balance...")
            cursor.execute("UPDATE accounts SET balance = balance + 300 WHERE id = 1")
            conn.commit()
            print("T2: Update committed")
    
    # Reset Alice's balance
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = 1000.00 WHERE id = 1")
        conn.commit()
    
    t1 = threading.Thread(target=transaction1)
    t2 = threading.Thread(target=transaction2)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

# =============================================================================
# 5. PHANTOM READ PROBLEM
# =============================================================================

def phantom_read_demo():
    """Demonstrates the phantom read problem"""
    print("\n=== PHANTOM READ PROBLEM DEMO ===")
    
    def transaction1():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            print("T1: First count of Electronics products...")
            cursor.execute("SELECT COUNT(*) FROM products WHERE category = 'Electronics'")
            count1 = cursor.fetchone()[0]
            print(f"T1: First count: {count1} products")
            
            # Simulate processing time
            time.sleep(3)
            
            print("T1: Second count of Electronics products...")
            cursor.execute("SELECT COUNT(*) FROM products WHERE category = 'Electronics'")
            count2 = cursor.fetchone()[0]
            print(f"T1: Second count: {count2} products")
            
            if count1 != count2:
                print("T1: PHANTOM READ! New records appeared between reads")
    
    def transaction2():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            time.sleep(1)  # Start after T1's first read
            
            print("T2: Inserting new Electronics product...")
            cursor.execute("INSERT INTO products (category, price) VALUES ('Electronics', 300.00)")
            conn.commit()
            print("T2: New product inserted")
    
    # Reset products table
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products")
        cursor.execute("INSERT INTO products (category, price) VALUES ('Electronics', 100.00)")
        cursor.execute("INSERT INTO products (category, price) VALUES ('Electronics', 200.00)")
        conn.commit()
    
    t1 = threading.Thread(target=transaction1)
    t2 = threading.Thread(target=transaction2)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

# =============================================================================
# SOLUTIONS USING TRANSACTION ISOLATION LEVELS
# =============================================================================

def demonstrate_solutions():
    """Demonstrates solutions using transaction isolation levels"""
    print("\n=== SOLUTIONS USING TRANSACTION ISOLATION ===")
    
    def serializable_transaction_example():
        """Example of using SERIALIZABLE isolation level"""
        print("Using SERIALIZABLE isolation level to prevent all problems:")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Set isolation level to SERIALIZABLE
            cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            conn.begin()
            
            try:
                cursor.execute("SELECT balance FROM accounts WHERE id = 1")
                balance = cursor.fetchone()[0]
                print(f"Current balance: {balance}")
                
                # This will prevent other transactions from interfering
                new_balance = balance + 100
                cursor.execute("UPDATE accounts SET balance = %s WHERE id = 1", (new_balance,))
                conn.commit()
                print("Transaction completed successfully")
                
            except Exception as e:
                print(f"Transaction failed: {e}")
                conn.rollback()
    
    def read_committed_example():
        """Example of using READ COMMITTED isolation level"""
        print("\nUsing READ COMMITTED to prevent dirty reads:")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
            conn.begin()
            
            cursor.execute("SELECT balance FROM accounts WHERE id = 1")
            balance = cursor.fetchone()[0]
            print(f"Balance read with READ COMMITTED: {balance}")
            
            conn.commit()
    
    serializable_transaction_example()
    read_committed_example()

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("Setting up database...")
    setup_database()
    
    print("Starting concurrency control problem demonstrations...\n")
    
    # Run all demonstrations
    lost_update_demo()
    time.sleep(1)
    
    dirty_read_demo()
    time.sleep(1)
    
    incorrect_summary_demo()
    time.sleep(1)
    
    nonrepeatable_read_demo()
    time.sleep(1)
    
    phantom_read_demo()
    time.sleep(1)
    
    demonstrate_solutions()
    
    print("\n=== SUMMARY ===")
    print("1. Lost Update: Two transactions update the same data, one update is lost")
    print("2. Dirty Read: Reading uncommitted changes that might be rolled back")
    print("3. Incorrect Summary: Aggregation during concurrent updates gives wrong results")
    print("4. Nonrepeatable Read: Same query returns different results within one transaction")
    print("5. Phantom Read: New records appear between identical queries")
    print("\nSolutions: Use appropriate transaction isolation levels and locking mechanisms")