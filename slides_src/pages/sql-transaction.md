---
title: SQL - Transaction
transition: fade
---


# Transaction

---

# Transaction

- Transactions are atomic units of work that can be committed or rolled back. When a transaction makes multiple changes to the database, either all the changes succeed when the transaction is committed, or all the changes are undone when the transaction is rolled back.

<!-- ---

# Atomic
- **What IS atomic:**
    - The SELECT operation itself (reading and summing the data)
    - The variable assignment happens in that single statement

```sql
START TRANSACTION;
INSERT INTO summary_table 
SELECT SUM(salary) FROM table1 WHERE type=1;
COMMIT;
```

- **What is NOT atomic**
    - The variable persists outside transaction control
    - Multiple statements using the variable aren't automatically atomic together

```sql
START TRANSACTION;
SELECT @A:=SUM(salary) FROM table1 WHERE type=1;  -- @A gets set
INSERT INTO log_table VALUES (@A);                -- Uses @A value
ROLLBACK;                                         -- Transaction rolls back

SELECT @A;  -- @A still contains the value! Not rolled back
```
 -->

---
layout: two-cols
---

# Syntax



```sql
START TRANSACTION
    [transaction_characteristic 
    [, transaction_characteristic] ...]

transaction_characteristic: {
    WITH CONSISTENT SNAPSHOT
  | READ WRITE
  | READ ONLY
}

BEGIN [WORK]
COMMIT [WORK] [AND [NO] CHAIN] [[NO] RELEASE]
ROLLBACK [WORK] [AND [NO] CHAIN] [[NO] RELEASE]
SET autocommit = {0 | 1}
```

::right::

<AutoFitText :max="25" :min="20">

These statements provide control over use of transactions:

- START TRANSACTION or BEGIN start a new transaction.

- COMMIT commits the current transaction, making its changes permanent.

- ROLLBACK rolls back the current transaction, canceling its changes.

- SET autocommit disables or enables the default autocommit mode for the current session.

</AutoFitText>


- https://dev.mysql.com/doc/refman/8.4/en/commit.html

---

 <span v-mark.highlight.yellow>By default, MySQL runs with autocommit mode enabled.</span> This means that, when not otherwise inside a transaction, each statement is atomic, as if it were surrounded by START TRANSACTION and COMMIT. You cannot use ROLLBACK to undo the effect; however, if an error occurs during statement execution, the statement is rolled back.

1. **Autocommit mode (default):** Each individual statement is automatically wrapped in its own transaction

```sql
INSERT INTO users VALUES ('John'); -- Automatically committed, cannot ROLLBACK
```

2. **Explicit transactions:** When you use START TRANSACTION...COMMIT, you CAN rollback before the COMMIT

```sql
START TRANSACTION;
INSERT INTO users VALUES ('John');  -- Not committed yet
ROLLBACK;  -- This WILL undo the INSERT
```
But once you COMMIT:

```sql
START TRANSACTION;
INSERT INTO users VALUES ('John');
COMMIT;  -- Now it's permanent
ROLLBACK;  -- This does NOTHING - already committed
```

---

<span v-mark.highlight.yellow>To disable autocommit mode implicitly for a single series of statements, use the START TRANSACTION statement:</span>

```sql
START TRANSACTION;
SELECT @A:=SUM(salary) FROM table1 WHERE type=1; 
UPDATE table2 SET summary=@A WHERE type=1; 
COMMIT;
```


<span v-mark.highlight.yellow>With START TRANSACTION, autocommit remains disabled until you end the transaction with COMMIT or ROLLBACK. The autocommit mode then reverts to its previous state.</span>

---

# Rollback

- Table `log_table` is rolls back after execute `ROLLBACK`

```sql
START TRANSACTION;
SELECT @A:=SUM(salary) FROM table1 WHERE type=1;  -- @A gets set
INSERT INTO log_table VALUES (@A);                -- Uses @A value
ROLLBACK;                                         -- Transaction rolls back

SELECT @A;  -- @A still contains the value! Not rolled back
```

---

# Disable autocommit

To disable autocommit mode explicitly, use the following statement:

```sql
SET autocommit=0;
```

---

# Programming language and autocommit

- **Python disable autocommit by default.** 

```python
conn = mysql.connector.connect(
    host='localhost',
    user='username', 
    password='password',
    database='mydb',
    autocommit=True
)

# or

conn.autocommit = True
```


---

# C# (.NET):

- SQL Server (SqlConnection): **Autocommit is enabled by default.** Each statement is automatically committed unless you explicitly start a transaction.
- MySQL (MySqlConnection): **Autocommit is enabled by default.**
- PostgreSQL (NpgsqlConnection): **Autocommit is enabled by default.**


```csharp
// Default behavior - autocommits immediately
using var connection = new SqlConnection(connectionString);
connection.Open();
var command = new SqlCommand("INSERT INTO users (name) VALUES ('John')", connection);
command.ExecuteNonQuery(); // Automatically committed

// To disable autocommit, use transactions
using var transaction = connection.BeginTransaction();
command.Transaction = transaction;
command.ExecuteNonQuery(); // Not committed yet
transaction.Commit(); // Now it's committed


// Disable autocommits via connection string
string connectionString = "Server=localhost;Database=mydb;Uid=user;Pwd=pass;AutoCommit=false;";
```

---

# PHP:

- MySQLi: **Autocommit is enabled by default.**
- PDO: **Autocommit is enabled by default.**

```php
// MySQLi - autocommit enabled by default
$mysqli = new mysqli("localhost", "user", "password", "database");
$mysqli->query("INSERT INTO users (name) VALUES ('John')"); // Auto-committed

// To disable autocommit
$mysqli->autocommit(false);
$mysqli->query("INSERT INTO users (name) VALUES ('Jane')"); // Not committed
$mysqli->commit(); // Now it's committed

// PDO - autocommit enabled by default
$pdo = new PDO("mysql:host=localhost;dbname=test", $user, $pass);
$pdo->exec("INSERT INTO users (name) VALUES ('John')"); // Auto-committed

// To use transactions (disable autocommit temporarily)
$pdo->beginTransaction();
$pdo->exec("INSERT INTO users (name) VALUES ('Jane')"); // Not committed
$pdo->commit(); // Now it's committed
```

--- 

# Python Example [Download](https://luckkrit.github.io/cos3103/python_transaction.rar)


```python


    def insert_order(self, orders:Orders, order_details:OrderDetails):

        with self.db.connection.cursor() as cursor:
            try:
                if not self.is_valid_customer_number(orders.customer_number):
                    raise ValueError(f"Customer number: {orders.customer_number} is not valid")
                if not self.is_valid_product_code(order_details.product_code):
                    raise ValueError(f"Product code: {order_details.product_code} is not valid")
                orders.order_number = self.get_order_number()
                order_details.order_number = orders.order_number
                affected_rows = cursor.execute("INSERT INTO orders (orderNumber,orderDate,requiredDate,shippedDate,status,comments,customerNumber) VALUES(%s,%s,%s,%s,%s,%s,%s);", (orders.order_number, orders.order_date, orders.required_date, orders.shipped_date, orders.status.value, orders.comments, orders.customer_number))
                # raise ValueError("Simulate error after insert table, rollback")
                affected_rows2 = cursor.execute("INSERT INTO orderdetails(orderNumber,productCode,quantityOrdered,priceEach,orderLineNumber) VALUES (%s,%s,%s,%s,%s);", (order_details.order_number, order_details.product_code, order_details.quantity_ordered, order_details.price_each, order_details.order_line_number))
                if affected_rows>0 and affected_rows2>0:
                    self.db.commit()
                else:
                    self.db.rollback()
                return affected_rows
            except Exception as e:
                print(f"Error: {e}")
                self.db.rollback()
                return -1
```