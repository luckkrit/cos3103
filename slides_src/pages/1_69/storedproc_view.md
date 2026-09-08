---
layout: section
transition: fade
---

## View, Functions, and Stored Procedure


---
layout: section
---

# Three Schema Architecture of DBMS

---
layout: two-cols
---
# Three Schema Architecture

- Used in modern web applications and enterprises system
- <span v-mark.highlight.red>It’s designed to separate the user's view of the data from the physical storage</span>
    - Scalability
    - Flexibility
    - Security

::right::

<div class="w-[350px]">

![3 Schema Arch](/images/sql-storedproc-views/three-schema-architecture.png)
</div>
---
layout: two-cols
---

# Three Schema Architecture

1. VIEW LEVEL
2. LOGICAL LEVEL
3. PHYSICAL LEVEL

::right::

<div class="w-[350px]">

![3 Schema Arch](/images/sql-storedproc-views/three-schema-architecture.png)
</div>
---
layout: two-cols
---

# Three Schema Architecture

1. VIEW LEVEL
    - Different users may see different views (V1, V2, ... Vm) of the same data. 
    - <span v-mark.highlight.red>Protects users from seeing irrelevant or sensitive data.</span>

2. LOGICAL LEVEL
3. PHYSICAL LEVEL

::right::


<div class="w-[350px]">

![3 Schema Arch](/images/sql-storedproc-views/three-schema-architecture.png)
</div>

---
layout: two-cols
---

# Three Schema Architecture


1. VIEW LEVEL
2. LOGICAL LEVEL
    - Describes the structure of the whole database using tables (relations) like R1, R2, ..., Rn.
    - <span v-mark.highlight.red>Provides a complete logical design of the database.</span>
3. PHYSICAL LEVEL

::right::

<div class="w-[350px]">

![3 Schema Arch](/images/sql-storedproc-views/three-schema-architecture.png)
</div>

---
layout: two-cols
---

# Three Schema Architecture


1. VIEW LEVEL
2. LOGICAL LEVEL
3. PHYSICAL LEVEL
    - The actual storage – how data is saved in files, indexes (F1, F2, ..., Fp) on the hard disk.
    - <span v-mark.highlight.red>Optimizes performance and space usage.</span>

::right::

<div class="w-[350px]">

![3 Schema Arch](/images/sql-storedproc-views/three-schema-architecture.png)
</div>

---

# Three Schema Architecture


- VL–LL Mapping: 
    - This shows how each view maps to the logical data.
    - <span v-mark.highlight.red>Ensures Logical Data Independence: </span>
        - Can change the logical structure (like adding a column) without changing user views.

- LL–PL Mapping:
    - Shows how the logical schema maps to the physical storage.
    - <span v-mark.highlight.red>Ensures Physical Data Independence:</span>
        - Can change how data is stored (e.g., use indexing or different files) without changing the logical structure.


---

# Example of Logical Data Independence

- Logical Data Independence

![Logical Data Independence](/images/sql-storedproc-views/logical_data_independence.png)


---

# Example of Logical Data Independence

- Logical Data Independence

![Logical Data Independence](/images/sql-storedproc-views/logical_data_independence2.png)

---

# Example of Physical Data Independence

- Physical Data Independence

![Physical Data Independence](/images/sql-storedproc-views/physical_data_independence.png)

---

# Example of Physical Data Independence

- Physical Data Independence

![Physical Data Independence](/images/sql-storedproc-views/physical_data_independence2.png)

---
layout: section
---

# View


---

# Views in SQL

- What is views?
    - View Logically represents subsets of data from one or more tables

- View = External View in Three schema architecture

<div class="w-[400px] mx-auto">

![Example Views](/images/sql-storedproc-views/ex_views.png)
</div>

---

# Querying a View

- How view works?

<div class="w-[500px] mx-auto">

![Querying a View](/images/sql-storedproc-views/views_querying.png)
</div>

--- 

# Why use Views?

- To restrict data access
- To make complex queries easy
- To provide data independence
- To present different views of the same data

---
layout: two-cols
---

# DML Limitations on Views

- You can perform `INSERT`, `UPDATE`, and `DELETE` on a view only if it is a simple view:
    - Based on a single table (no `JOIN`)

    - Has no `GROUP BY`, `HAVING`, or `DISTINCT`

    - Has no aggregate functions
        - `AVG()`, `SUM()`, `COUNT()`, etc.

    - Has no calculated/derived columns
        - `salary * 12`

    - Includes all `NOT NULL` columns from the base table (for `INSERT`)

::right::


 **DML (Data Manipulation Language)** : `SELECT`, `INSERT`, `UPDATE`, `DELETE`


---

# How to create a View

```sql
CREATE [OR REPLACE] VIEW [db_name.]view_name [(column_list)]
AS
    select-statement;
```

- `CREATE VIEW` specify the name of the view that you want to create after the keywords
- `REPLACE` option if you want to replace an existing view if the view already exists. If the view does not exist, the `OR REPLACE` has no effect.


---
layout: two-cols-title
---

::left::


- By default search path will be public

```sql
-- set default schema to public

SET search_path TO public, classicmodels;

-- view is created in public

CREATE VIEW salePerOrder AS
SELECT 
    orderNumber, 
    SUM(quantityOrdered * priceEach) AS total
FROM orderDetails
GROUP BY orderNumber;

```


::right::

- Specify other schema like `classicmodels` 

```sql

CREATE VIEW classicmodels.salePerOrder AS
SELECT 
    orderNumber, 
    SUM(quantityOrdered * priceEach) AS total
FROM orderDetails
GROUP BY orderNumber;
```

- Another way

```sql
SET search_path TO classicmodels;

CREATE VIEW salePerOrder AS
SELECT 
    orderNumber, 
    SUM(quantityOrdered * priceEach) AS total
FROM orderDetails
GROUP BY orderNumber;
```


---
layout: two-cols-title
---


::left::

# Example 1

```sql
CREATE VIEW classicmodels.salePerOrder AS
    SELECT 
        orderNumber, 
        SUM(quantityOrdered * priceEach) total
    FROM
        orderDetails
    GROUP by orderNumber
    ORDER BY total DESC;
```

<div class="w-[150px] mx-auto">

![Sale Per Order View](/images/sql-storedproc-views/salePerOrderView.png)

</div>
::right::

<div class="w-[250px] mx-auto">


![storedproc_view_2026-09-05-19-27-13](/images/storedproc_view/storedproc_view_2026-09-05-19-27-13.png)
</div>


<div class="w-[250px] mx-auto">


![storedproc_view_2026-09-05-19-26-24](/images/storedproc_view/storedproc_view_2026-09-05-19-26-24.png)
</div>

---
layout: two-cols-title
---

::left::

# Example 2

```sql
CREATE VIEW classicmodels.bigSalesOrder AS
    SELECT 
        orderNumber, 
        ROUND(total,2) as total
    FROM
        salePerOrder
    WHERE
        total > 60000;

```

::right::

```sql
SELECT orderNumber, total FROM classicmodels.bigSalesOrder;
```

![storedproc_view_2026-09-06-14-22-05](/images/storedproc_view/storedproc_view_2026-09-06-14-22-05.png)


---
layout: two-cols-title
---

::title::
[Creating View with JOIN]{class="text-2xl"}

::left::

```sql
CREATE OR REPLACE VIEW classicmodels.customerOrders AS 
    SELECT orderNumber, customerName,  
    SUM(quantityOrdered * priceEach) total 
    FROM orderDetails 
    INNER JOIN orders o USING (orderNumber) 
    INNER JOIN customers USING (customerNumber) 
    GROUP BY orderNumber, customerName;
```

![1_69_db_three_schema_architecture_2026-09-06-15-37-19](/images/storedproc_view/1_69_db_three_schema_architecture_2026-09-06-15-37-19.png){.w-full}

::right::

```sql
SELECT * FROM customerOrders ORDER BY total DESC;
```

![1_69_db_three_schema_architecture_2026-09-06-15-42-47](/images/storedproc_view/1_69_db_three_schema_architecture_2026-09-06-15-42-47.png){.w-[300px]}



- In PostgreSQL, when using GROUP BY, every non-aggregated column in SELECT must appear in GROUP BY.

::default::

---
layout: two-cols-title
---

::title::
[Creating a View with sub query]{class="text-2xl"}

::left::

```sql
CREATE OR REPLACE VIEW classicmodels.aboveAvgProducts 
(vproductCode,vproductName,vbuyPrice)
AS
    SELECT 
        productCode, 
        productName, 
        buyPrice
    FROM
        products
    WHERE
        buyPrice > (
            SELECT AVG(buyPrice)
            FROM products)
    ORDER BY buyPrice DESC;
```

::right::

```sql
SELECT * FROM aboveAvgProducts;
```

![1_69_db_three_schema_architecture_2026-09-06-16-24-37](/images/storedproc_view/1_69_db_three_schema_architecture_2026-09-06-16-24-37.png)
::default::

---
layout: two-cols-title
---

::title::
[Update a view with a subquery]{class="text-2xl"}

::left::

- A view is **updatable** if it does NOT have any of the following:
    - DISTINCT in the SELECT
    - GROUP BY or HAVING
    - Aggregate functions (SUM, COUNT, AVG, MAX, MIN, etc.)
    - Set operators (UNION, INTERSECT, EXCEPT/MINUS)
    - Multiple tables in the FROM clause (i.e., no joins — must be based on a single table)
    - Calculated/derived columns (e.g., price * qty AS total, or any expression instead of a plain column reference)


::right::

```sql
UPDATE classicmodels.customerOrders
SET  customername = 'XXXX’ 
WHERE  ordernumber = '10165';
```

[ERROR: cannot update view "customerorders" Views containing GROUP BY are not automatically updatable]{.text-red-500}

::default::


---

# Drop View

```sql
DROP VIEW classicmodels.aboveavgproducts;
```

---
layout: two-cols-title
---

::title::
[PL/pgSQL Overview]{class="text-2xl"}

::left::

- PL/pgSQL is PostgreSQL's built-in procedural language, designed to:
    - Create **functions, procedures, and triggers**
    - Add **control structures** (IF, LOOP, etc.) to SQL
    - Perform **complex computations**
    - Use all SQL data types, operators, and functions
    - Run **trusted** by default — safe for regular users


::right::

### Why use it?

- Runs **inside the server** — no back-and-forth between client and database
- Fewer network round trips → **better performance**
- Group multiple queries + logic into a single call

### Quick note
- Installed by **default** since PostgreSQL 9.0

::default::

---
layout: two-cols-title
---

::title::
[Anonymous Block]{class="text-2xl"}

::left::


- `DO` statement itself - the SQL command that runs a procedural block immediately, without saving it
- no name, can't be called again, not stored in the database



::right::

### Both styles are working

- Style1

```sql
DO LANGUAGE plpgsql $$
BEGIN
    RAISE NOTICE 'Hello';
END;
$$;
```

- Style 2
```sql
DO $$
BEGIN
    RAISE NOTICE 'Hello';
END;
$$ LANGUAGE plpgsql;
```

::default::

---

## Other Languages that PogreSQL support

<CsvTable><pre>
Language	Based on	Typical use case
PL/pgSQL	Custom (Oracle PL/SQL-inspired)	Default, most widely used, what we've been discussing
PL/Tcl	Tcl	Lightweight scripting, older/legacy usage
PL/Perl	Perl	Text processing, regex-heavy logic, string manipulation
PL/Python (PL/Python3)	Python	Data science/ML integration, calling Python libraries directly from SQL
</pre></CsvTable>

---

## Example of Anonymous Block

```sql
DO $$
DECLARE
    v_var1 INTEGER := 10;
    v_var2 INTEGER;
BEGIN
    -- SQL statements
    v_var2 := v_var1 * 2;

    -- control flow (IF, LOOP, CASE, etc.)
    IF v_var2 > 15 THEN
        RAISE NOTICE 'v_var2 (%) is greater than 15', v_var2;
    ELSE
        RAISE NOTICE 'v_var2 (%) is 15 or less', v_var2;
    END IF;

EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'Error occurred: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
```

```
NOTICE:  v_var2 (20) is greater than 15
DO

Query returned successfully in 102 msec.
```

---

## คำสั่งพื้นฐาน

- EXIT
- WHILE
- LOOP
- IF
- CASE
- CURSOR

---

## Data Types - Numeric & Boolean

| Type              | ขนาด              | ใช้เมื่อไหร่      |
|-------------------|-------------------|-------------------|
| smallint          | 2 bytes           | ค่าน้อย ๆ         |
| integer           | 4 bytes           | ทั่วไป            |
| bigint            | 8 bytes           | id ใหญ่           |
| numeric(p,s)      | precision สูง     | เงิน              |
| decimal(p,s)      | เหมือน numeric    | เงิน              |
| real              | float 4 byte      | ค่าทศนิยมทั่วไป   |
| double precision  | float 8 byte      | คำนวณหนัก         |
| Boolean           |                   | True, FALSE, Null |


---
layout: two-cols-title
---

::title::
[Example]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    v_smallint       smallint := 100;
    v_integer        integer := 50000;
    v_bigint         bigint := 9000000000;
    v_numeric        numeric(10,2) := 1234.56;
    v_decimal        decimal(10,2) := 9876.54;
    v_real           real := 3.14;
    v_double         double precision := 3.14159265358979;
    v_boolean        boolean := true;
BEGIN
    RAISE NOTICE 'smallint: %', v_smallint;
    RAISE NOTICE 'integer: %', v_integer;
    RAISE NOTICE 'bigint: %', v_bigint;
    RAISE NOTICE 'numeric(10,2): %', v_numeric;
    RAISE NOTICE 'decimal(10,2): %', v_decimal;
    RAISE NOTICE 'real: %', v_real;
    RAISE NOTICE 'double precision: %', v_double;
    RAISE NOTICE 'boolean: %', v_boolean;
END;
$$ LANGUAGE plpgsql;
```
::right::


```
NOTICE:  smallint: 100
NOTICE:  integer: 50000
NOTICE:  bigint: 9000000000
NOTICE:  numeric(10,2): 1234.56
NOTICE:  decimal(10,2): 9876.54
NOTICE:  real: 3.14
NOTICE:  double precision: 3.14159265358979
NOTICE:  boolean: t
DO

Query returned successfully in 90 msec.
```
::default::

---
layout: two-cols-title
---

::title::
[Data Type - Datetime]{class="text-2xl"}

::left::

| Type        | ใช้เมื่อไหร่      |
|-------------|-------------------|
| date        | วันที่อย่างเดียว  |
| time        | เวลาอย่างเดียว    |
| timestamp   | ไม่มี timezone    |
| timestamptz | มี timezone       |

::right::

```sql
DO $$
DECLARE
    v_date         date := '2026-09-06';
    v_time        time := '14:30:00';
    v_timestamp   timestamp := '2026-09-06 14:30:00';
    v_timestamptz timestamptz := '2026-09-06 14:30:00+07';
BEGIN
    RAISE NOTICE 'date: %', v_date;
    RAISE NOTICE 'time: %', v_time;
    RAISE NOTICE 'timestamp (no timezone): %', v_timestamp;
    RAISE NOTICE 'timestamptz (with timezone): %', 
    v_timestamptz;
END;
$$ LANGUAGE plpgsql;
```

::default::

```
NOTICE:  date: 2026-09-06
NOTICE:  time: 14:30:00
NOTICE:  timestamp (no timezone): 2026-09-06 14:30:00
NOTICE:  timestamptz (with timezone): 2026-09-06 14:30:00+07
DO

Query returned successfully in 102 msec.
```

---
layout: two-cols-title
---

::title::
[Timezone vs. Timestamp]{class="text-2xl"}

::left::

| ตำแหน่งข้อมูล        | ค่าที่แสดง                          | หมายเหตุ         |
|----------------------|--------------------------------------|------------------|
| คุณเห็น (session)    | 2026-02-21 15:33:39.629805+07        | Bangkok time     |
| เก็บจริงบน disk      | 2026-02-21 08:33:39.629805+00        | UTC              |

::right::

![storedproc_view_2026-09-06-18-47-26](/images/storedproc_view/storedproc_view_2026-09-06-18-47-26.png)

::default::

[UTC (Coordinated Universal Time) คือเวลามาตรฐานกลางของโลก ในระบบฐานข้อมูลอย่าง PostgreSQL ไม่มี timezone offset (+7, -5 ฯลฯ)]{.text-red-500}

---

## Row Type


| Type          | What it holds                        | Structure known ahead of time? |
|---------------|----------------------------------------|-------------------------------|
| `RECORD`      | Any row, shape decided at runtime      | ❌ No                          |
| `%ROWTYPE`    | A full row matching one specific table | ✅ Yes                         |
| `%TYPE`       | A single column's data type            | ✅ Yes                         |

**Key takeaway:**
- Use `%TYPE` when you only need **one column's** type (auto-updates if the column type changes)
- Use `%ROWTYPE` when you need a **whole row** from a known table
- Use `RECORD` when the query's shape is **not known until runtime** (e.g. dynamic queries, generic loops)


---

## Example : RECORD


```sql

DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT productCode, productName FROM products LOOP
        RAISE NOTICE '%: %', r.productCode, r.productName;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

- OUTPUT

```
NOTICE:  S10_1678: 1969 Harley Davidson Ultimate Chopper
NOTICE:  S10_1949: 1952 Alpine Renault 1300
NOTICE:  S10_2016: 1996 Moto Guzzi 1100i
NOTICE:  S10_4698: 2003 Harley-Davidson Eagle Drag Bike
NOTICE:  S10_4757: 1972 Alfa Romeo GTA
```

---

## Example : %ROWTYPE

```sql

DO $$
DECLARE
    prod products%ROWTYPE;
BEGIN
    SELECT * INTO prod FROM products 
    WHERE productCode = 'S10_1949';
    RAISE NOTICE 'Name: %, Price: %', prod.productName, prod.buyPrice;
END;
$$ LANGUAGE plpgsql;

```

- OUTPUT

```
NOTICE:  Name: 1952 Alpine Renault 1300, Price: 98.58
DO

Query returned successfully in 98 msec.
```

---

## Example : %TYPE

```sql
DO $$
DECLARE
    v_price products.buyPrice%TYPE;
BEGIN
    SELECT buyPrice INTO v_price FROM products 
    WHERE productCode = 'S10_1949';
    RAISE NOTICE 'Price: %', v_price;
END;
$$ LANGUAGE plpgsql;


```

- OUTPUT

```
NOTICE:  Price: 98.58
DO

Query returned successfully in 108 msec.
```

---

## strict_multi_assignment ช่วยจับ bug แบบ "จำนวนคอลัมน์ไม่ตรง" ได้

```sql
SET plpgsql.extra_errors TO 'strict_multi_assignment';
DO $$
DECLARE
    v_price products.buyPrice%TYPE;
BEGIN
    SELECT buyPrice,productCode INTO v_price FROM products 
    WHERE productCode = 'S10_1949';
    RAISE NOTICE 'Price: %', v_price;
END;
$$ LANGUAGE plpgsql;

```

- OUTPUT

```
ERROR:  number of source and target fields in assignment does not match
strict_multi_assignment check of extra_errors is active. 

SQL state: 42804
Detail: strict_multi_assignment check of extra_errors is active.
Hint: Make sure the query returns the exact list of columns.
Context: PL/pgSQL function inline_code_block line 5 at SQL statement
```

---

## Solution


```sql
DO $$
DECLARE
    v_price products.buyPrice%TYPE;
	v_code products.productCode%TYPE;
BEGIN
    SELECT buyPrice,productCode INTO v_price,v_code FROM products 
    WHERE productCode = 'S10_1949';
    RAISE NOTICE 'Price: %, Code: %', v_price, v_code;
END;
$$ LANGUAGE plpgsql;


```

- OUTPUT

```
NOTICE:  Price: 98.58, Code: S10_1949
DO

Query returned successfully in 109 msec.
```

---

## Example: FETCH ใส่ค่าตาม "ตำแหน่ง" ไม่ใช่ตาม "ชื่อ"

```sql

DO $$ -- SET plpgsql.extra_errors TO 'strict_multi_assignment'; จะทำให้ Error ขึ้นมา
DECLARE
    cur_products CURSOR FOR
        SELECT productCode, buyPrice FROM products WHERE buyPrice > 50; -- แก้ด้วย วิธีที่ 1 ใช้ SELECT * 
    v_record products%ROWTYPE; -- แก้ด้วยวิธีที่ 2 ใช้ RECORD แทน
BEGIN
    OPEN cur_products;
    LOOP
        FETCH cur_products INTO v_record;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'ROWTYPE -> Code: %, Price: %', v_record.productCode, v_record.buyPrice;
    END LOOP;
    CLOSE cur_products;
END;
$$;
```

- OUTPUT

```
NOTICE:  ROWTYPE -> Code: S700_3167, Price: <NULL>
NOTICE:  ROWTYPE -> Code: S700_3505, Price: <NULL>
NOTICE:  ROWTYPE -> Code: S700_3962, Price: <NULL>
DO

Query returned successfully in 95 msec.
```

---

## Multiple Assignments

```sql
DO $$
DECLARE
    a integer;
    b integer;
    c text;
BEGIN
    SELECT 1, 2, 'hello' INTO a, b, c;
    RAISE NOTICE 'a=%, b=%, c=%', a, b, c;
END;
$$;
```

```
NOTICE:  a=1, b=2, c=hello
DO

Query returned successfully in 85 msec.
```

---
layout: two-cols-title
---

::title::
[Implicit vs Explicit Type Casting]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    -- Implicit cast: PostgreSQL silently 
    -- rounds numeric -> integer
    v_implicit integer := 10.7;

    -- Explicit casts: conversion is visible in the code
    -- rounds -> 11
    v_cast      integer := (10.7)::integer;      
    -- rounds -> 11 (standard SQL syntax)
    v_cast_std  integer := CAST(10.7 AS integer); 
    -- rounds on purpose -> 11
    v_round     integer := ROUND(10.7)::integer;  
    -- cuts decimal -> 10
    v_trunc     integer := TRUNC(10.7)::integer;  
BEGIN
    RAISE NOTICE 'Implicit (v_num := 10.7):   %', v_implicit;
    RAISE NOTICE 'Explicit (::integer):       %', v_cast;
    RAISE NOTICE 'Explicit (CAST AS integer): %', v_cast_std;
    RAISE NOTICE 'Explicit ROUND():           %', v_round;
    RAISE NOTICE 'Explicit TRUNC():           %', v_trunc;
END;
$$;
```

::right::

```
NOTICE:  Implicit (v_num := 10.7):   11
NOTICE:  Explicit (::integer):       11
NOTICE:  Explicit (CAST AS integer): 11
NOTICE:  Explicit ROUND():           11
NOTICE:  Explicit TRUNC():           10
DO

Query returned successfully in 102 msec.
```

::default::

---
layout: two-cols-title
---

::title::
[Floor vs. Ceil vs. Round]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    v_pos numeric := 10.5;
    v_neg numeric := -10.5;
BEGIN
    RAISE NOTICE '--- Positive value: % ---', v_pos;
    -- 11 (nearest, ties away from zero)
    RAISE NOTICE 'ROUND: %', ROUND(v_pos); 
    -- 10 (toward -infinity)
    RAISE NOTICE 'FLOOR: %', FLOOR(v_pos);  
    -- 11 (toward +infinity)
    RAISE NOTICE 'CEIL:  %', CEIL(v_pos);   

    RAISE NOTICE '--- Negative value: % ---', v_neg;
    -- -11 (nearest, ties away from zero)
    RAISE NOTICE 'ROUND: %', ROUND(v_neg);  
    -- -11 (toward -infinity)
    RAISE NOTICE 'FLOOR: %', FLOOR(v_neg);  
    -- -10 (toward +infinity)
    RAISE NOTICE 'CEIL:  %', CEIL(v_neg);   
END;
$$;
```

::right::

```
NOTICE:  --- Positive value: 10.5 ---
NOTICE:  ROUND: 11
NOTICE:  FLOOR: 10
NOTICE:  CEIL:  11
NOTICE:  --- Negative value: -10.5 ---
NOTICE:  ROUND: -11
NOTICE:  FLOOR: -11
NOTICE:  CEIL:  -10
DO

Query returned successfully in 106 msec.
```

::default::

---
layout: two-cols-title
---

::title::
[Example: IF - ELSE IF - ELSE]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    v_score integer := 75;
    v_grade text;
BEGIN
    IF v_score >= 90 THEN
        v_grade := 'A';
    ELSIF v_score >= 80 THEN
        v_grade := 'B';
    ELSIF v_score >= 70 THEN
        v_grade := 'C';
    ELSIF v_score >= 60 THEN
        v_grade := 'D';
    ELSE
        v_grade := 'F';
    END IF;

    RAISE NOTICE 'Score: %, Grade: %', v_score, v_grade;
END;
$$;
```

::right::

```
NOTICE:  Score: 75, Grade: C
DO

Query returned successfully in 88 msec.
```

::default::


---
layout: two-cols-title
---

::title::
[Example: FOR]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    v_num integer;
    v_result text;
BEGIN
    FOR v_num IN 1..5 LOOP
        
        v_result := v_num;
		raise notice '%',v_result;

        
    END LOOP;
END;
$$;

```

::right::

```
NOTICE:  1
NOTICE:  2
NOTICE:  3
NOTICE:  4
NOTICE:  5
DO

Query returned successfully in 83 msec.
```

::default::

---
layout: two-cols-title
---

::title::
[Example: While]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    v_count integer := 1;
BEGIN
    WHILE v_count <= 5 LOOP
        RAISE NOTICE 'Count: %', v_count;
        v_count := v_count + 1;
    END LOOP;
END;
$$;
```

::right::

```
NOTICE:  Count: 1
NOTICE:  Count: 2
NOTICE:  Count: 3
NOTICE:  Count: 4
NOTICE:  Count: 5
DO

Query returned successfully in 89 msec.
```

::default::

---
layout: two-cols-title
---

::title::
[Example: Loop + EXIT When]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    v_count integer := 1;
BEGIN
    LOOP
        -- ทำงานก่อนเช็คเงื่อนไข
        RAISE NOTICE 'Count: %', v_count;   
        v_count := v_count + 1;

        -- เช็คเงื่อนไขท้ายลูป (เหมือน DO WHILE)
        EXIT WHEN v_count > 5;   
    END LOOP;
END;
$$;
```

::right::

```
NOTICE:  Count: 1
NOTICE:  Count: 2
NOTICE:  Count: 3
NOTICE:  Count: 4
NOTICE:  Count: 5
DO

Query returned successfully in 82 msec.
```

::default::

---
layout: two-cols-title
---

::title::
[Example: While + Exit]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    v_count integer := 1;
BEGIN
    WHILE v_count <= 100 LOOP   -- เงื่อนไขหลักของ WHILE
        RAISE NOTICE 'Count: %', v_count;

        IF v_count = 5 THEN
            RAISE NOTICE 
            'Found target at count=5, exiting early';
            EXIT;  -- ออกจากลูปทันที ไม่สนใจเงื่อนไข WHILE เลย
        END IF;

        v_count := v_count + 1;
    END LOOP;

    RAISE NOTICE 'Loop ended, final count = %', v_count;
END;
$$;
```

::right::


```
NOTICE:  Count: 1
NOTICE:  Count: 2
NOTICE:  Count: 3
NOTICE:  Count: 4
NOTICE:  Count: 5
NOTICE:  Found target at count=5, exiting early
NOTICE:  Loop ended, final count = 5
DO

Query returned successfully in 103 msec.
```

::default::

---
layout: two-cols-title
---

::title::
[Example: CASE]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    v_num integer := NULL; -- เป็น NULL ทำให้เข้า ELSE
    v_result text;
BEGIN
    CASE 
        WHEN v_num % 2 = 0 THEN
            v_result := 'Even';
        WHEN v_num % 2 = 1 THEN
            v_result := 'Odd';
        ELSE
            v_result := 'Unknown';
    END CASE;
    RAISE NOTICE 'Number: %, Type: %', v_num, v_result;
END;
$$;
```

::right::

```
NOTICE:  Number: <NULL>, Type: Unknown
DO

Query returned successfully in 106 msec.
```

::default::

---
layout: two-cols-title
---

::title::
[Example: CASE]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    v_num integer := 10;
    v_result text;
BEGIN
    CASE 
        WHEN v_num % 2 = 0 THEN
            v_result := 'Even';
        WHEN v_num % 2 = 1 THEN
            v_result := 'Odd';
        ELSE
            v_result := 'Unknown';
    END CASE;
    RAISE NOTICE 'Number: %, Type: %', v_num, v_result;
END;
$$;
```

::right::

```
NOTICE:  Number: 10, Type: Even
DO

Query returned successfully in 92 msec.
```

::default::


---
layout: two-cols-title
---

::title::
[Example: Case & For]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    rec record;
BEGIN
    FOR rec IN
	         (SELECT 
	            ordernumber,
	            status,
	            CASE 
	                WHEN status = 'Shipped' THEN 'Completed'
	                WHEN status = 'Disputed' THEN 'Problem'
	                ELSE 'Pending'
	            END AS status_group
	            FROM orders)
	        LOOP
	  
       RAISE NOTICE 'Order: %, Group: %',
                     rec.ordernumber,
                     rec.status_group;
    END LOOP;
END;
$$;

```

::right::

```
NOTICE:  Order: 10100, Group: Completed
NOTICE:  Order: 10101, Group: Completed
NOTICE:  Order: 10102, Group: Completed
NOTICE:  Order: 10103, Group: Completed
NOTICE:  Order: 10104, Group: Completed
NOTICE:  Order: 10105, Group: Completed
NOTICE:  Order: 10106, Group: Completed
NOTICE:  Order: 10107, Group: Completed
NOTICE:  Order: 10108, Group: Completed
NOTICE:  Order: 10109, Group: Completed
NOTICE:  Order: 10110, Group: Completed
NOTICE:  Order: 10111, Group: Completed
```

::default::


---
layout: two-cols-title
---

::title::
[Example: For & Group By]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    rec record;
BEGIN
    FOR rec IN
        SELECT 
            status,
            CASE 
                WHEN status = 'Shipped' THEN 'Completed'
                WHEN status = 'Disputed' THEN 'Problem'
                ELSE 'Pending'
            END AS status_group,
            COUNT(ordernumber) AS order_count
        FROM orders
        GROUP BY status
    LOOP
        RAISE NOTICE 'Group: %, Count: %', 
        rec.status_group, rec.order_count;
    END LOOP;
END;
$$;
```

::right::

```
NOTICE:  Group: Completed, Count: 303
NOTICE:  Group: Pending, Count: 6
NOTICE:  Group: Problem, Count: 3
NOTICE:  Group: Pending, Count: 6
NOTICE:  Group: Pending, Count: 4
NOTICE:  Group: Pending, Count: 4
DO

Query returned successfully in 106 msec.

```

- `status` ถูกใส่ไว้ใน `GROUP BY` ดังนั้น `status_group` (ซึ่งคำนวณจาก `status` เพียงอย่างเดียว) ไม่ต้องใส่ซ้ำ
- `COUNT(ordernumber)` ไม่ต้องใส่ใน `GROUP BY` เพราะเป็น aggregate function อยู่แล้ว

::default::

---
layout: two-cols-title
---

::title::
[Example: For & Distinct]{class="text-2xl"}

::left::

```sql
DO $$
DECLARE
    rec record;
BEGIN
    FOR rec IN
        SELECT DISTINCT
            status,
            CASE 
                WHEN status = 'Shipped' THEN 'Completed'
                WHEN status = 'Disputed' THEN 'Problem'
                ELSE 'Pending'
            END AS status_group
        FROM orders
    LOOP
        RAISE NOTICE 'Status: %, Group: %', rec.status, 
        rec.status_group;
    END LOOP;
END;
$$;
```

::right::

```
NOTICE:  Status: On Hold, Group: Pending
NOTICE:  Status: In Process, Group: Pending
NOTICE:  Status: Resolved, Group: Pending
NOTICE:  Status: Disputed, Group: Problem
NOTICE:  Status: Cancelled, Group: Pending
NOTICE:  Status: Shipped, Group: Completed
DO

Query returned successfully in 97 msec.
```

::default::


---

## Cursor


- **Cursor** = เครื่องมือ iterate ผ่านแต่ละ row ที่ query ส่งกลับมา เพื่อประมวลผลทีละแถว

**PostgreSQL cursor มีคุณสมบัติ 3 อย่าง:**

| คุณสมบัติ | ความหมาย |
|---|---|
| **Read-only** | แก้ไขข้อมูลผ่าน cursor โดยตรงไม่ได้ |
| **Non-scrollable** | fetch ได้ทิศทางเดียวตามลำดับที่ query กำหนด — ย้อนกลับ, ข้าม, หรือกระโดดไป row ใดไม่ได้ |
| **Asensitive** | ไม่ copy ข้อมูล — ชี้ไปที่ข้อมูลจริง เร็วกว่า insensitive cursor แต่ถ้ามีการแก้ไขข้อมูลจาก connection อื่นระหว่างใช้ cursor ก็จะเห็นผลกระทบนั้นด้วย |

**สรุปสั้น:** เร็ว แต่ไม่ปลอดภัยถ้ามีคนอื่นแก้ข้อมูลพร้อมกัน จึงไม่ควรใช้ cursor แก้ไขข้อมูลที่กำลังถูกอ่านอยู่


---

## How cursor works?

![storedproc_view_2026-09-06-19-54-05](/images/storedproc_view/storedproc_view_2026-09-06-19-54-05.png){.mx-auto}

---

### 1. DECLARE — ประกาศตัวแปรและ cursor

```sql
DECLARE
    v_result   return_datatype := initial_value;
    v_record   record;

    cur_name CURSOR FOR
        SELECT column_list
        FROM table_name
        WHERE condition;
```

- ประกาศตัวแปรที่จะใช้เก็บผลลัพธ์ (`v_result`, `v_record`)
- ประกาศ cursor (`cur_name`) พร้อมผูก query ไว้ล่วงหน้า — **แต่ query ยังไม่ถูกรันตอนนี้**

### 2. OPEN — เปิด cursor
```sql
OPEN cur_name;
```

- ตรงนี้คือจุดที่ query จริง ๆ เริ่มถูก execute
- PostgreSQL เตรียม "ตัวชี้" (pointer) ไปที่แถวแรกของผลลัพธ์ แต่ยังไม่ได้ดึงข้อมูลออกมา

---

### 3. FETCH — ดึงข้อมูลทีละแถว
```sql
LOOP
    FETCH cur_name INTO v_record;
    EXIT WHEN NOT FOUND;
    -- ทำงานกับ v_record ตรงนี้
END LOOP;
```

- `FETCH` ดึงข้อมูล 1 แถวจาก cursor เข้าตัวแปร `v_record`
- ทุกครั้งที่ `FETCH` ตัวชี้จะเลื่อนไปแถวถัดไปอัตโนมัติ (เดินหน้าทางเดียว — ตรงกับ **non-scrollable** ที่เรียนมาก่อนหน้า)

### 4. EMPTY? (เงื่อนไขจบ loop)
```sql
EXIT WHEN NOT FOUND;
```

- ถ้า `FETCH` ไม่พบแถวใหม่ (ดึงมาหมดแล้ว) → `NOT FOUND` จะเป็น `TRUE` → ออกจาก loop
- ถ้ายังมีแถวเหลือ → กลับไป `FETCH` ต่อ (ตรงกับลูก "No" ใน diagram ที่วนกลับไปหา FETCH)

---

### 5. CLOSE — ปิด cursor
```sql
CLOSE cur_name;
```

- คืนทรัพยากรที่ cursor ใช้อยู่กลับสู่ระบบ
- **ต้องปิดเสมอ** แม้ query จะ error หรือ loop จบตามปกติ — ถ้าไม่ปิด cursor อาจค้างและกินทรัพยากร connection

---

### ตัวอย่างจริงกับตาราง `products`

```sql
DO $$
DECLARE
    -- Step 1: Declare variables and cursor
    v_total    numeric := 0;
    v_record   record;
    cur_products CURSOR FOR
        SELECT productCode, buyPrice
        FROM products
        WHERE buyPrice > 50;
BEGIN
    -- Step 2: Open cursor (query starts executing here)
    OPEN cur_products;
    -- Step 3-4: Loop fetch, exit when no more rows (EMPTY?)
    LOOP
        FETCH cur_products INTO v_record;
        EXIT WHEN NOT FOUND;
        -- Business logic: accumulate total and print each row
        v_total := v_total + v_record.buyPrice;
        RAISE NOTICE 'Code: %, Price: %', v_record.productCode, v_record.buyPrice;
    END LOOP;
    -- Step 5: Close cursor (always, to release resources)
    CLOSE cur_products;
    -- Step 6: Return/print final result
    RAISE NOTICE 'Total: %', v_total;
END;
$$;
```

---
layout: two-cols-title
---

::title::
[การใช้ While + FOUND]{class="text-2xl"}


::left::

```sql
DO $$
DECLARE
    cur_products CURSOR FOR
        SELECT productCode, buyPrice FROM products 
        WHERE buyPrice > 50;
    v_record  RECORD;
BEGIN
    OPEN cur_products;
    FETCH cur_products INTO v_record;

    IF NOT FOUND THEN
        RAISE NOTICE 'ไม่พบข้อมูลใด ๆ ตามเงื่อนไข';
    ELSE
        WHILE FOUND LOOP
            RAISE NOTICE 'Code: %, Price: %', 
            v_record.productCode, v_record.buyPrice;
            FETCH cur_products INTO v_record;
        END LOOP;
    END IF;

    CLOSE cur_products;
END;
$$;
```


::right::

```
NOTICE:  Code: S32_4485, Price: 56.13
NOTICE:  Code: S50_1392, Price: 68.29
NOTICE:  Code: S700_1691, Price: 51.15
NOTICE:  Code: S700_2466, Price: 68.8
NOTICE:  Code: S700_2834, Price: 59.33
NOTICE:  Code: S700_3167, Price: 54.4
NOTICE:  Code: S700_3505, Price: 51.09
NOTICE:  Code: S700_3962, Price: 53.63
DO

Query returned successfully in 93 msec.
```

::default::

---
layout: two-cols-title
---

::title::
[ลืม EXIT WHEN NOT FOUND]{class="text-2xl"}

::left::

- ถ้าลืมเงื่อนไขนี้ใน loop จะเกิด **infinite loop** ทันที เพราะไม่มีจุดออกจาก loop เลย

### ❌ ผิด — ไม่มีทางออกจาก loop
```sql
DO $$
DECLARE
    v_record   record;
    cur_products CURSOR FOR
        SELECT productCode, buyPrice FROM products 
        WHERE buyPrice > 50;
BEGIN
    OPEN cur_products;

    LOOP
        FETCH cur_products INTO v_record;
        -- ลืม EXIT WHEN NOT FOUND!
        RAISE NOTICE 'LOOPING';
    END LOOP;

    CLOSE cur_products;
END;
$$;
```

- พอ `FETCH` ดึงข้อมูลจนหมดแล้ว `v_record` จะกลายเป็น `NULL` แต่ loop ยังวนต่อไปเรื่อย ๆ **ไม่มีที่สิ้นสุด**
- ต้อง**กด Cancel query เอง** หรือปิด session ทิ้ง ไม่งั้นค้างตลอดไป


::right::

### ✅ ถูก — มี EXIT WHEN NOT FOUND
```sql
LOOP
    FETCH cur_products INTO v_record;
    EXIT WHEN NOT FOUND;   -- จุดตรวจสอบ "EMPTY?" ใน diagram
    RAISE NOTICE 'Code: %', v_record.productCode;
END LOOP;
```

```sql
DO $$
DECLARE
    v_record   record;
    cur_products CURSOR FOR
        SELECT productCode, buyPrice FROM products 
        WHERE buyPrice > 50;
BEGIN
    OPEN cur_products;
    LOOP
        FETCH cur_products INTO v_record;
        -- หยุดเอง เพราะ v_record เป็น NULL
        RAISE NOTICE 'Code: %', v_record.productCode;
    END LOOP;
    CLOSE cur_products;
END;
$$;


```

::default::


---

## ลืม CLOSE cursor

```sql
DO $$
DECLARE
    v_record   record;
    cur_products CURSOR FOR
        SELECT productCode FROM products;
BEGIN
    OPEN cur_products;
    LOOP
        FETCH cur_products INTO v_record;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'Code: %', v_record.productCode;
    END LOOP;
    -- ลืม CLOSE cur_products!
END;
$$;
```

- Cursor ที่เปิดค้างไว้จะยังกิน**ทรัพยากรของ connection** อยู่จนกว่า session จะจบ
- ถ้าเปิด cursor จำนวนมากโดยไม่ปิด อาจทำให้ connection เต็มหรือ database ทำงานช้าลง
- **แนวทางที่ปลอดภัยกว่า:** ใช้ `FOR r IN SELECT ... LOOP` (implicit cursor) แทน เพราะ PostgreSQL จะ open/fetch/close ให้อัตโนมัติ ไม่มีทางลืม

---


## Implicit cursor

```sql
DO $$
DECLARE
    r record;
BEGIN
    FOR r IN
        SELECT productCode, buyPrice
        FROM products
        WHERE buyPrice > 50
    LOOP
        RAISE NOTICE 'Code: %, Price: %', r.productCode, r.buyPrice;
    END LOOP;
END;
$$;
```

- ผลลัพธ์เหมือนกันทุกประการกับ explicit cursor version แต่โค้ดสั้นกว่า ปลอดภัยกว่า (ไม่มีทางลืม CLOSE หรือ EXIT WHEN NOT FOUND) — เหมาะกับการใช้งานทั่วไป ส่วน explicit cursor จะเก็บไว้ใช้เฉพาะตอนที่ต้องการควบคุมแบบละเอียด เช่น fetch เป็น batch หรือเปิด cursor ค้างไว้ข้าม transaction


---
layout: two-cols-title
---

::title::

## Explicit Cursor with Batch Processing

::left::

```sql
DO $$
DECLARE
    cur_products CURSOR FOR
        SELECT productCode, buyPrice FROM products 
		WHERE buyPrice > 50 ORDER BY productCode;
    v_record   products%ROWTYPE;
    v_batch    products%ROWTYPE[] := '{}';
    v_count    int := 0;
BEGIN
    OPEN cur_products;
    LOOP
        FETCH cur_products INTO v_record;
        EXIT WHEN NOT FOUND;

        v_batch := v_batch || v_record;
        v_count := v_count + 1;

        IF v_count = 10 THEN
            RAISE NOTICE 'Got a batch of % rows', 
			array_length(v_batch, 1);
            v_batch := '{}';
            v_count := 0;
        END IF;
    END LOOP;

```

::right:: 

```sql

    IF v_count > 0 THEN
        RAISE NOTICE 'Final partial batch: % rows', v_count;
    END IF;

    CLOSE cur_products;
END;
$$;
```

- OUTPUT

```
NOTICE:  Got a batch of 10 rows
NOTICE:  Got a batch of 10 rows
NOTICE:  Got a batch of 10 rows
NOTICE:  Got a batch of 10 rows
NOTICE:  Got a batch of 10 rows
NOTICE:  Got a batch of 10 rows
NOTICE:  Final partial batch: 2 rows
DO

Query returned successfully in 98 msec.
```

---

# Cursor + Exception Handling

⚠️ ถ้า error เกิดขึ้นกลาง loop โดยไม่มี `EXCEPTION` block → **cursor จะไม่ถูก CLOSE**

### ❌ ไม่ปลอดภัย — ไม่มีการดัก error
```sql
DO $$
DECLARE
    cur_products CURSOR FOR
        SELECT productCode, buyPrice FROM products WHERE buyPrice > 50;
    v_record RECORD;
BEGIN
    OPEN cur_products;
    LOOP
        FETCH cur_products INTO v_record;
        EXIT WHEN NOT FOUND;

        RAISE NOTICE '%', v_record.buyPrice / 0;  -- เกิด error ตรงนี้

    END LOOP;
    CLOSE cur_products;   -- ❌ ไม่ถูกรัน ถ้า error เกิดก่อนหน้า
END;
$$;
```

---

### ✅ ปลอดภัย — CLOSE cursor ทั้งใน flow ปกติและใน EXCEPTION


```sql
DO $$
DECLARE
    cur_products CURSOR FOR
        SELECT * FROM products WHERE buyPrice > 50;
    v_record RECORD;
BEGIN
    OPEN cur_products;
    BEGIN
        LOOP
            FETCH cur_products INTO v_record;
            EXIT WHEN NOT FOUND;
            RAISE NOTICE '%', v_record.buyPrice / 0;
        END LOOP;
        CLOSE cur_products;
    EXCEPTION
        WHEN others THEN
            RAISE NOTICE 'Error occurred: %', SQLERRM;
            -- ไม่ต้อง CLOSE ตรงนี้ เพราะ cursor ถูกปิดไปแล้วโดย savepoint rollback
    END;
END;
$$;

```

```
NOTICE:  Error occurred: division by zero
DO

Query returned successfully in 96 msec.
```



---

## สรุป

| คุณสมบัติที่เคยเรียน | จุดที่เห็นในวงจรนี้ |
|---|---|
| **Non-scrollable** | `FETCH` เดินหน้าทางเดียวเท่านั้น — ถ้าพลาดจุด `EXIT WHEN NOT FOUND` ก็ไม่มีทาง "ถอยกลับ" ได้ มีแต่วนลูปไปเรื่อย ๆ |
| **Read-only** | ระหว่าง loop ทำได้แค่ *อ่าน* ค่าจาก `v_record` เท่านั้น แก้ข้อมูลในตารางผ่าน cursor โดยตรงไม่ได้ |
| **Asensitive** | เพราะ cursor ไม่ copy ข้อมูล ถ้ามี connection อื่นแก้ไข/ลบแถวระหว่างที่ loop กำลังรันอยู่ ผลลัพธ์ที่ `FETCH` ได้อาจเปลี่ยนไปโดยไม่รู้ตัว — เป็นอีกเหตุผลที่ควรปิด cursor (CLOSE) ให้เร็วที่สุดเท่าที่จะทำได้ ไม่ปล่อยค้างไว้นาน |


---

## Exercise

1. ใช้พวก IF / ELSIF / ELSE + datatype integer, text
> เขียน anonymous block ประกาศตัวแปร v_age integer := 17;
> - แล้วใช้ IF...ELSIF...ELSE แบ่งกลุ่มอายุ:
>    - น้อยกว่า 13 → "เด็ก"
>    - 13–19 → "วัยรุ่น"
>    - 20–59 → "ผู้ใหญ่"
>    - 60 ขึ้นไป → "ผู้สูงอายุ"
> - ให้ print ผลลัพธ์ด้วย RAISE NOTICE เป็นประโยคสมบูรณ์ เช่น "อายุ 17 ปี จัดอยู่ในกลุ่ม: วัยรุ่น"

---

2. FOR loop (range) + CASE + datatype boolean

> -  ใช้ FOR v_num IN 1..15 LOOP วนตัวเลข 1 ถึง 15
> - เก็บผลเช็คการหารลงตัวไว้ในตัวแปร boolean สองตัว (v_div3, v_div5) แล้วใช้ CASE แยก 4 กรณี:
>   - หารด้วย 3 และ 5 ลงตัว → print "<เลข> หารด้วยทั้ง 3 และ 5 ลงตัว"
>   - หารด้วย 3 ลงตัวอย่างเดียว → print "<เลข> หารด้วย 3 ลงตัว"
>   - หารด้วย 5 ลงตัวอย่างเดียว → print "<เลข> หารด้วย 5 ลงตัว"
>   - ไม่เข้าเงื่อนไขไหนเลย → print "<เลข> หารด้วย 3 และ 5 ไม่ลงตัว"

---

3. ใช้พวก WHILE loop + datatype numeric

> - ประกาศ v_balance numeric := 1000; 
> - และ v_year integer := 0; 
> - จำลองดอกเบี้ยทบต้น 5% ต่อปี (v_balance := v_balance * 1.05;) 
> - ใช้ WHILE วนจนกว่า v_balance จะเกิน 2000 พร้อมนับว่าใช้กี่ปี แล้ว print จำนวนปีที่ใช้ และยอดเงินสุดท้าย (ปัดทศนิยม 2 ตำแหน่งด้วย ROUND)

4. ใช้พวก FOREACH กับ array + datatype text[]

> - ประกาศ `v_fruits text[] := ARRAY['apple','banana','mango','durian'];`
> - ใช้ FOREACH v_item IN ARRAY v_fruits LOOP 
> - วน print ชื่อผลไม้ทีละตัว พร้อมความยาวของชื่อ (LENGTH(v_item)) เช่น "apple มีความยาว 5 ตัวอักษร"

---

5. ใช้พวก CURSOR + IF + datatype RECORD

> - ใช้ตาราง products (จาก classicmodels ที่ใช้ในคาบเรียน) 
> - เขียน cursor ดึง productCode, productName, buyPrice เฉพาะแถวที่ buyPrice > 50 
> - วนด้วย LOOP/FETCH/EXIT WHEN NOT FOUND 
> - แล้วใช้ IF เช็คว่า buyPrice > 100 หรือไม่
>   - ถ้าใช่ print ว่า "สินค้าราคาสูง" 
>   - ถ้าไม่ print "สินค้าราคาปานกลาง" 
> - พร้อมชื่อและราคาสินค้า อย่าลืม CLOSE cursor ท้ายบล็อก

---

## Solution

ข้อ 1.

```sql
DO $$
DECLARE
    v_age integer := 17;
BEGIN
    IF v_age < 13 THEN
		raise notice 'เด็ก';
	ELSIF v_age <= 19 THEN
		raise notice 'วัยรุ่น';
	ELSIF v_age <= 59 THEN
		raise notice 'ผู้ใหญ่';
	ELSE
		raise notice 'ผู้สูงอายุ';
	END IF;
END;
$$;
```

```
NOTICE:  วัยรุ่น
DO

Query returned successfully in 86 msec.
```

---
layout: two-cols
---


::left::

ข้อ 2.
```sql
DO $$
DECLARE
    v_div3 integer;
	v_div5 integer;
	v_num integer;
BEGIN
    FOR v_num in 1..15 LOOP
	   CASE 
	   	WHEN v_num % 3 = 0 and 
		   MOD(v_num, 5) = 0 then
		   raise notice '% หายด้วย 3 และ 5 ลงตัว', v_num;
		WHEN v_num % 3 = 0 then
		   raise notice '% หายด้วย 3 ลงตัว', v_num;
		WHEN v_num % 5 = 0 then
		   raise notice '% หายด้วย 5 ลงตัว', v_num;
		ELSE
			raise notice '% หารด้วย 3 และ 5 ไม่ลงตัว', v_num;
		END CASE;
	END LOOP;
END;
$$;


```

::right::
```
NOTICE:  1 หารด้วย 3 และ 5 ไม่ลงตัว
NOTICE:  2 หารด้วย 3 และ 5 ไม่ลงตัว
NOTICE:  3 หายด้วย 3 ลงตัว
NOTICE:  4 หารด้วย 3 และ 5 ไม่ลงตัว
NOTICE:  5 หายด้วย 5 ลงตัว
NOTICE:  6 หายด้วย 3 ลงตัว
NOTICE:  7 หารด้วย 3 และ 5 ไม่ลงตัว
NOTICE:  8 หารด้วย 3 และ 5 ไม่ลงตัว
NOTICE:  9 หายด้วย 3 ลงตัว
NOTICE:  10 หายด้วย 5 ลงตัว
NOTICE:  11 หารด้วย 3 และ 5 ไม่ลงตัว
NOTICE:  12 หายด้วย 3 ลงตัว
NOTICE:  13 หารด้วย 3 และ 5 ไม่ลงตัว
NOTICE:  14 หารด้วย 3 และ 5 ไม่ลงตัว
NOTICE:  15 หายด้วย 3 และ 5 ลงตัว
DO

Query returned successfully in 90 msec.
```

---
layout: two-cols
---

::left::

ข้อ 3.

```sql
DO $$
DECLARE
    v_balance numeric := 1000;
	v_year integer := 0;
BEGIN
    WHILE v_balance < 2000 LOOP
	   v_balance := v_balance * 1.05;
	   v_year := v_year + 1;
	END LOOP;
	raise notice 'ใช้เวลา % ปี และยอดเงินสุดท้าย % บาท', 
    v_year, ROUND(v_balance,2);
END;
$$;
```

::right::

```
NOTICE:  ใช้เวลา 15 ปี และยอดเงินสุดท้าย 2078.93 บาท
DO

Query returned successfully in 100 msec.
```

---

ข้อ 4.

```sql
DO $$
DECLARE
    v_fruits text[] := ARRAY['apple','banana','mango','durian'];
	v_item text;
BEGIN
    FOREACH v_item in ARRAY v_fruits LOOP
		raise notice 'ชื่อ % ยาว % ตัวอักษร', v_item,LENGTH(v_item);
	END LOOP;
END;
$$;


```

```
NOTICE:  ชื่อ apple ยาว 5 ตัวอักษร
NOTICE:  ชื่อ banana ยาว 6 ตัวอักษร
NOTICE:  ชื่อ mango ยาว 5 ตัวอักษร
NOTICE:  ชื่อ durian ยาว 6 ตัวอักษร
DO

Query returned successfully in 90 msec.
```

---
layout: two-cols
---

::left::
ข้อ 5.

```sql
DO $$
DECLARE
    v_product RECORD;
	c_product CURSOR FOR
	SELECT productCode, productName, buyPrice 
	FROM classicmodels.products WHERE buyPrice > 50;
BEGIN
    OPEN c_product;
	BEGIN
		LOOP
			FETCH c_product INTO v_product;
			EXIT WHEN NOT FOUND;

			IF v_product.buyPrice > 100 THEN
				raise notice '% ราคา % บาท -> สินค้าราคาสูง', 
                v_product.productName, v_product.buyPrice;
			ELSE
				raise notice '% ราคา % บาท -> สินค้าราคาปานกลาง',
                 v_product.productName, v_product.buyPrice;
			END IF;

```

::right::

```sql
		END LOOP;
		CLOSE c_product;
	EXCEPTION
		WHEN others THEN
			RAISE NOTICE 'Error occurred: %', SQLERRM;
	END;
END;
$$;
```

```
NOTICE:  America West Airlines B757-200 ราคา 68.8 บาท -> สินค้าราคาปานกลาง
NOTICE:  ATA: B757-300 ราคา 59.33 บาท -> สินค้าราคาปานกลาง
NOTICE:  F/A 18 Hornet 1/72 ราคา 54.4 บาท -> สินค้าราคาปานกลาง
NOTICE:  The Titanic ราคา 51.09 บาท -> สินค้าราคาปานกลาง
NOTICE:  The Queen Mary ราคา 53.63 บาท -> สินค้าราคาปานกลาง
DO

Query returned successfully in 65 msec.
```

---

## Stored Procedures in PostgreSQL

- A stored procedure contains a sequence of SQL commands stored in the database catalog so that it can be invoked later by a program

- Stored procedures:
  - Procedures
  - Function

---

## Stored Procedures Advantages (PostgreSQL)

- **Reduce network traffic**
  - แอปพลิเคชันส่งแค่ชื่อและพารามิเตอร์ของ stored procedure แทนที่จะส่ง SQL statement ยาว ๆ หลายคำสั่งไปยัง PostgreSQL server

- **Centralize business logic in the database**
  - เขียน business logic ไว้ที่เดียว ใช้ซ้ำได้จากหลายแอปพลิเคชัน ลดความซ้ำซ้อนของ logic และทำให้ฐานข้อมูลสอดคล้องกันมากขึ้น

- **Make database more secure**
  - Database administrator สามารถให้สิทธิ์เข้าถึงเฉพาะ stored procedure โดยไม่ต้องให้สิทธิ์เข้าถึงตารางข้อมูลโดยตรง

---

## Stored Procedures Disadvantages (PostgreSQL)

- **Resource usage**
  - ถ้าใช้ stored procedure จำนวนมาก การใช้ memory ต่อ connection จะเพิ่มขึ้น
  - Logic ที่ซับซ้อนหรือมี loop จำนวนมากใน PL/pgSQL ก็เพิ่ม CPU usage ได้เช่นกัน

- **Debugging**
  - PostgreSQL ไม่มี debugger แบบ step-by-step ในตัว ต้องอาศัย `RAISE NOTICE` เป็นหลัก หรือ extension เสริมอย่าง `pldebugger` ซึ่งยังไม่สะดวกเท่าเครื่องมือ debug ของภาษาโปรแกรมทั่วไป

- **Maintenance**
  - ต้องใช้ทักษะเฉพาะทาง (PL/pgSQL) ซึ่งไม่ใช่ผู้พัฒนาแอปพลิเคชันทุกคนจะถนัด
  - อาจสร้างปัญหาในการพัฒนาและดูแลรักษาในระยะยาว ถ้าทีมไม่มีคนที่ชำนาญ PL/pgSQL

---

## ความแตกต่าง Procedure vs. Function

| | Function | Procedure |
|---|---|---|
| **ค่าที่คืนกลับ** | ต้องคืนค่าเสมอ (หรือ `void`) | ไม่คืนค่าโดยตรง — ส่งกลับได้ผ่าน `INOUT` เท่านั้น |
| **การเรียกใช้** | เรียกใน expression: `SELECT my_func(x);` | ต้องใช้ `CALL`: `CALL my_proc(x);` |
| **Transaction control** | ❌ ใช้ `COMMIT`/`ROLLBACK` ข้างในไม่ได้ | ✅ ใช้ `COMMIT`/`ROLLBACK` ข้างในได้ |
| **Parameter** | ใช้ `RETURNS` กำหนด output type | ใช้ `INOUT` แทน `RETURNS` |
| **ใช้ในที่ไหนได้บ้าง** | ใช้ใน `SELECT`, `WHERE`, computed column ได้ | เรียกแบบ standalone เท่านั้น ใช้ใน expression ไม่ได้ |

---
layout: two-cols
---

::left::
## Enable pldebugger

0. เช็คว่าได้ติดตั้งหรือยัง `SHOW shared_preload_libraries;`
1. หา config file `SHOW config_file;`
2. แก้ config file `C:\Program Files\PostgreSQL\18\data\postgresql.conf`
3. ใส่ `shared_preload_libraries = 'plugin_debugger'`

```
# - Shared Library Preloading -

#local_preload_libraries = ''
#session_preload_libraries = ''
#shared_preload_libraries = ''  # (change requires restart)
#jit_provider = 'llvmjit'		# JIT library to use
shared_preload_libraries = 'plugin_debugger'
```

4. restart service ของ postgresql 

::right::

![storedproc_view_2026-09-06-22-13-26](/images/storedproc_view/storedproc_view_2026-09-06-22-13-26.png){.w-[400px]}

5. รันคำสั่ง `CREATE EXTENSION pldbgapi;` แค่ 1 ครั้ง



---

## Create storedprocedure

```sql
CREATE OR REPLACE PROCEDURE procedure_name(parameter_list)
LANGUAGE plpgsql
AS $$
BEGIN
    statements;
END;
$$;
```

---

## Example

- Create

```sql
CREATE OR REPLACE  PROCEDURE classicmodels.test_proc()
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'Hello';
END;
$$;
```

- Call

```sql
CALL classicmodels.test_proc();
```

- Drop

```sql
DROP PROCEDURE IF EXISTS classicmodels.test_proc();
```

---

## ประเภทของ parameter

| Mode | รับค่าเข้า | ส่งค่ากลับ | ตอนเรียกต้องใส่ค่าไหม |
|---|---|---|---|
| `IN` (default) | ✅ | ❌ | ✅ ต้องใส่ |
| `OUT` | ❌ | ✅ | ต้องใส่ placeholder (เช่น `NULL`) |
| `INOUT` | ✅ | ✅ | ✅ ต้องใส่ค่าเริ่มต้น |

---

## Example: IN 

```sql
CREATE OR REPLACE PROCEDURE classicmodels.greet(IN p_name varchar)
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'What is your name?';
    RAISE NOTICE 'My name is %', p_name;
END;
$$;

CALL greet('Krit');
```

```
NOTICE:  What is your name?
NOTICE:  My name is Krit
CALL

Query returned successfully in 79 msec.
```

---

## Debuging IN parameter 

![Debug IN parameter](/images/storedproc_view/pgAdmin4_sWUvYf1mk2.gif)

---

## Example: OUT

```sql
-- ============================
-- OUT: ส่งชื่อกลับออกมา (ไม่ต้องใส่ค่าตอนเรียก)
-- ============================
CREATE OR REPLACE PROCEDURE classicmodels.greet_out(OUT p_message varchar)
LANGUAGE plpgsql
AS $$
BEGIN
    p_message := 'What is your name? My name is Krit';
END;
$$;

CALL greet_out(NULL);
```

<CsvTable><pre>
"p_message"
"What is your name? My name is Krit"
</pre></CsvTable>

---
layout: two-cols
---

::left::
## Example: INOUT

```sql
-- ============================
-- INOUT: รับชื่อเข้ามา แล้วส่งข้อความทักทายกลับออกไปในตัวแปรเดียวกัน
-- ============================
CREATE OR REPLACE PROCEDURE classicmodels.greet_inout(
    INOUT p_name varchar)
LANGUAGE plpgsql
AS $$
BEGIN
    p_name := 'What is your name? My name is ' || p_name;
END;
$$;

```


::right::

- Call ผ่าน Anonymous block output จะเป็น text

```sql
DO $$
DECLARE
    p_name varchar := 'Krit';
BEGIN
    CALL classicmodels.greet_inout(p_name);
    RAISE NOTICE '%', p_name;   
END;
$$ LANGUAGE plpgsql;
```


```
NOTICE:  What is your name? My name is Krit
DO

Query returned successfully in 95 msec.
```

- OUTPUT เป็น table

```sql
CALL greet_inout('Krit');
```

<CsvTable><pre>
"p_name"
"What is your name? My name is Krit"
</pre></CsvTable>

---

## Default Parameter

- `DEFAULT` parameter คือการกำหนดค่าตั้งต้นให้พารามิเตอร์ ถ้าตอน `CALL` ไม่ได้ส่งค่านั้นมา Postgres จะใช้ค่า default แทนให้เองอัตโนมัติ ไม่ต้องพิมพ์ค่าให้ครบทุกตัวเสมอไป

```sql
CREATE OR REPLACE PROCEDURE classicmodels.getTotalOrder(
    OUT totalorder integer,
    p_customerNumber integer DEFAULT NULL,
    p_status text DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*) INTO totalorder
    FROM classicmodels.orders
    WHERE (p_customerNumber IS NULL OR customerNumber = p_customerNumber)
      AND (p_status IS NULL OR status = p_status);
END;
$$;
```

---

## กฎสำคัญ 2 ข้อที่ต้องจำ (โดยเฉพาะกับ Procedure ที่มี OUT)

- กฎที่ 1: DEFAULT ต้องอยู่ท้ายสุดของกลุ่ม IN/INOUT เสมอ

**พารามิเตอร์ที่ไม่มี default ห้ามอยู่หลังตัวที่มี default**

```sql
-- ❌ ผิด
CREATE PROCEDURE bad(a integer DEFAULT 1, b integer)

-- ✅ ถูก
CREATE PROCEDURE good(a integer, b integer DEFAULT 1)
```

---

## กฎสำคัญ 2 ข้อที่ต้องจำ (โดยเฉพาะกับ Procedure ที่มี OUT)

- กฎที่ 2: OUT parameter ต้องอยู่ "ก่อน" พารามิเตอร์ที่มี DEFAULT เสมอ

เพราะ OUT ไม่สามารถมี default ได้ (มันไม่ได้รับค่าจากผู้เรียก) จึงต้องอยู่ก่อนกลุ่มที่มี default

```sql
-- ❌ ผิด (error 42P13 ที่คุณเจอ)
CREATE PROCEDURE bad(
    p_customerNumber integer DEFAULT NULL,
    OUT totalorder integer
)

-- ✅ ถูก
CREATE PROCEDURE good(
    OUT totalorder integer,
    p_customerNumber integer DEFAULT NULL
)
```



---

## Positional Parameter vs. Named Parameter

```sql
CREATE OR REPLACE PROCEDURE classicmodels.getTotalOrder(
    OUT totalorder integer,
    p_customerNumber integer DEFAULT NULL,
    p_status text DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*) INTO totalorder
    FROM classicmodels.orders
    WHERE (p_customerNumber IS NULL OR customerNumber = p_customerNumber)
      AND (p_status IS NULL OR status = p_status);
END;
$$;
```

1. เรียกแบบ Positional (เรียงตามตำแหน่ง)

```sql
-- Call by positional parameter
CALL classicmodels.getTotalOrder(NULL, 103, 'Shipped');
```

<CsvTable><pre>
"totalorder"
3
</pre></CsvTable>

---


## Positional Parameter vs. Named Parameter

2. เรียกแบบ Named (ระบุชื่อ และสลับตำแหน่งได้)

```sql
CALL classicmodels.getTotalOrder(
    p_customerNumber => 103,
    p_status => 'Shipped',
    totalorder => NULL
);
```

<CsvTable><pre>
"totalorder"
3
</pre></CsvTable>

---

## Positional Parameter vs. Named Parameter

3. ข้าม DEFAULT parameter

```sql
CALL classicmodels.getTotalOrder(totalorder => NULL);
-- p_customerNumber และ p_status ใช้ค่า DEFAULT (NULL) อัตโนมัติ
```

<CsvTable><pre>
"totalorder"
3
</pre></CsvTable>

---

## Overloaded Procedure

- สมมติจะสร้าง getTotalOrder แบบ overload 3 รูปแบบ: ไม่ filter เลย, filter ตาม customer, filter ตาม customer + status

1. DROP Overloaded Procedure

ต้องระบุ parameter type ให้ตรงกับ signature ที่จะลบ เพราะชื่อเดียวกันแต่มีหลายตัว ถ้าไม่ระบุ Postgres จะไม่รู้ว่าจะลบตัวไหน

```sql
-- ลบทีละ signature ตามชนิด parameter (ไม่ต้องระบุชื่อ param หรือ OUT)
DROP PROCEDURE IF EXISTS classicmodels.getTotalOrder();
DROP PROCEDURE IF EXISTS classicmodels.getTotalOrder(integer);
DROP PROCEDURE IF EXISTS classicmodels.getTotalOrder(integer, text);
```

⚠️ หมายเหตุ: `OUT` parameter ไม่นับเป็นส่วนหนึ่งของ signature ตอน DROP (นับเฉพาะ IN/INOUT) ดังนั้นไม่ต้องใส่ type ของ `OUT totalorder integer` ใน `DROP`

⚠️ ข้อควรระวังตอน DROP: ถ้าใช้ `DROP PROCEDURE classicmodels.getTotalOrder;` เฉย ๆ โดยไม่ระบุ parameter type และมี 3 signature พร้อมกัน จะได้ error ว่า `procedure name "getTotalOrder" is not unique` ต้องระบุ type ให้ชัดเสมอเวลามี overload

---

2. CREATE Overloaded Procedure (3 แบบ)

แบบที่ 1 — ไม่มี filter เลย

```sql
CREATE OR REPLACE PROCEDURE classicmodels.getTotalOrder(
    OUT totalorder integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*) INTO totalorder
    FROM classicmodels.orders;
END;
$$;
```

---

2. CREATE Overloaded Procedure (3 แบบ)

แบบที่ 2 — filter ตาม customerNumber

```sql
CREATE OR REPLACE PROCEDURE classicmodels.getTotalOrder(
    OUT totalorder integer,
    p_customerNumber integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*) INTO totalorder
    FROM classicmodels.orders
    WHERE customerNumber = p_customerNumber;
END;
$$;
```

---

2. CREATE Overloaded Procedure (3 แบบ)

แบบที่ 3 — filter ตาม customerNumber + status

```sql
CREATE OR REPLACE PROCEDURE classicmodels.getTotalOrder(
    OUT totalorder integer,
    p_customerNumber integer,
    p_status text
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*) INTO totalorder
    FROM classicmodels.orders
    WHERE customerNumber = p_customerNumber
      AND status = p_status;
END;
$$;
```

---

3. CALL Overloaded Procedure

Postgres จะเลือก overload ให้เองจาก จำนวน argument ที่ส่งเข้าไป

```sql
-- เรียกแบบที่ 1: ไม่ filter (0 argument นอกจาก OUT)
CALL classicmodels.getTotalOrder(NULL);

-- เรียกแบบที่ 2: filter customer (1 argument นอกจาก OUT)
CALL classicmodels.getTotalOrder(NULL, 103);

-- เรียกแบบที่ 3: filter customer + status (2 argument นอกจาก OUT)
CALL classicmodels.getTotalOrder(NULL, 103, 'Shipped');
```

---

3. CALL Overloaded Procedure


เรียกแบบ Named Parameter (อ่านง่ายกว่า ไม่งงว่าตัวไหนคือตัวไหน)


```sql
-- แบบที่ 1
CALL classicmodels.getTotalOrder(totalorder => NULL);

-- แบบที่ 2
CALL classicmodels.getTotalOrder(
    totalorder => NULL,
    p_customerNumber => 103
);

-- แบบที่ 3
CALL classicmodels.getTotalOrder(
    totalorder => NULL,
    p_customerNumber => 103,
    p_status => 'Shipped'
);
```

---

## Example

```sql
DROP PROCEDURE IF EXISTS classicmodels.countOrderStatus(OUT vtotal integer,
      OUT vShipped integer,OUT vDisputed integer);

CREATE OR REPLACE PROCEDURE classicmodels.countorderstatus(
    OUT vtotal integer,
    OUT vShipped integer,
    OUT vDisputed integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT 
        COUNT(*),
        SUM(CASE WHEN status = 'Shipped'  THEN 1 ELSE 0 END),
        SUM(CASE WHEN status = 'Disputed' THEN 1 ELSE 0 END)
    INTO vtotal, vShipped, vDisputed
    FROM classicmodels.orders;

    RAISE NOTICE 'vtotal: %, vShipped: %, vDisputed: %',
                 vtotal, vShipped, vDisputed;
END;
$$;

CALL classicmodels.countorderstatus(vtotal=>NULL,vShipped=>NULL,vDisputed=>NULL);

```

---

## Debugging OUT parameter


![Debugging OUT parameter](/images/storedproc_view/pgAdmin4_fZbLjQ8VXy.gif)

---

## Functions 

- Declared using the following syntax:

```sql
CREATE FUNCTION name ([parameter_list])
RETURNS Type
LANGUAGE plpgsql
AS $$
BEGIN
    statements;
END;
$$;
```

---

## Return Types

1. Scalar เช่น integer, text, boolean, numeric, date
2. void
3. TABLE
4. Others (ไม่ได้สอน)

---
layout: two-cols-title
---


::title::
## Scalar Type

::left::


- integer

```sql
CREATE OR REPLACE FUNCTION 
classicmodels.get_order_count(p_customerNumber integer)
RETURNS integer
LANGUAGE plpgsql
AS $$
DECLARE
    v_count integer;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM classicmodels.orders
    WHERE customerNumber = p_customerNumber;

    RETURN v_count;
END;
$$;
```

```sql
SELECT classicmodels.get_order_count(103);
```

::right::

- numeric

```sql
CREATE OR REPLACE FUNCTION 
classicmodels.get_order_total(p_orderNumber integer)
RETURNS numeric
LANGUAGE plpgsql
AS $$
DECLARE
    v_total numeric;
BEGIN
    SELECT SUM(quantityOrdered * priceEach) INTO v_total
    FROM classicmodels.orderdetails
    WHERE orderNumber = p_orderNumber;

    RETURN v_total;
END;
$$;
```

```sql
SELECT classicmodels.get_order_total(10100);
```

---
layout: two-cols-title
---

::title::

## Scalar Type

::left::

- Boolean

```sql
CREATE OR REPLACE FUNCTION 
classicmodels.is_customer_active(p_customerNumber integer)
RETURNS boolean
LANGUAGE plpgsql
AS $$
DECLARE
    v_count integer;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM classicmodels.orders
    WHERE customerNumber = p_customerNumber
      AND orderDate > CURRENT_DATE - INTERVAL '1 year';

    RETURN v_count > 0;
END;
$$;
```

```sql
SELECT classicmodels.is_customer_active(103);
-- ใช้ใน WHERE ก็ได้ เพราะ scalar function เรียกใน expression ได้
SELECT * FROM classicmodels.customers
WHERE classicmodels.is_customer_active(customerNumber);
```

::right::

- text

```sql
CREATE OR REPLACE FUNCTION 
classicmodels.get_customer_status(p_customerNumber integer)
RETURNS text
LANGUAGE plpgsql
AS $$
DECLARE
    v_count integer;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM classicmodels.orders
    WHERE customerNumber = p_customerNumber;

    IF v_count = 0 THEN
        RETURN 'No orders';
    ELSIF v_count < 5 THEN
        RETURN 'Occasional';
    ELSE
        RETURN 'Frequent';
    END IF;
END;
$$;
```

```sql
SELECT classicmodels.get_customer_status(103);
```


---

## Scalar Type

- date

```sql
CREATE OR REPLACE FUNCTION classicmodels.get_last_order_date(p_customerNumber integer)
RETURNS date
LANGUAGE plpgsql
AS $$
DECLARE
    v_last_date date;
BEGIN
    SELECT MAX(orderDate) INTO v_last_date
    FROM classicmodels.orders
    WHERE customerNumber = p_customerNumber;

    RETURN v_last_date;
END;
$$;
```

```sql
SELECT classicmodels.get_last_order_date(103);
```

---

## void

```sql
CREATE OR REPLACE FUNCTION classicmodels.check_order_status(p_orderNumber integer)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'Checking order number: %', p_orderNumber;
END;
$$;
```

```sql
SELECT classicmodels.check_order_status(10100);
```

---

## Return 1 Row (Composite Type)

- ถ้ารู้ว่าจะ Return Table customer แค่ 1 Row ก็ยังไม่ต้องใช้

```sql
CREATE OR REPLACE FUNCTION classicmodels.get_customer(p_customerNumber integer)
RETURNS classicmodels.customers
LANGUAGE plpgsql
AS $$
DECLARE
    v_customer classicmodels.customers;
BEGIN
    SELECT * INTO v_customer FROM classicmodels.customers WHERE customerNumber = p_customerNumber;
    RETURN v_customer;
END;
$$;
```


---

## Return หลาย Row

- แต่ถ้ารู้ว่าจะ Return Table customer หลาย Row ก็ใช้ SETOF แทนได้

```sql
CREATE OR REPLACE FUNCTION classicmodels.get_customers_by_country(p_country text)
RETURNS SETOF classicmodels.customers
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM classicmodels.customers
    WHERE country = p_country;
END;
$$;
```

---

## Return หลาย Row มีคอลัมน์ใหม่

- แต่ถ้ารู้ว่าจะ Return Table customer แต่มีการเพิ่ม column ใหม่ขึ้นมา

```sql
CREATE OR REPLACE FUNCTION classicmodels.get_customer_order_summary(p_country text)
RETURNS TABLE(
    customerNumber integer,
    customerName varchar,
    order_count bigint
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.customerNumber,
        c.customerName,
        COUNT(o.orderNumber) AS order_count
    FROM classicmodels.customers c
    LEFT JOIN classicmodels.orders o ON c.customerNumber = o.customerNumber
    WHERE c.country = p_country
    GROUP BY c.customerNumber, c.customerName;
END;
$$;
```

---

## การเรียกใช้

```sql
-- (composite type, 1 row) — เรียกแบบ scalar-like
SELECT * FROM classicmodels.get_customer(103);
-- หรือ
SELECT classicmodels.get_customer(103);  -- ได้ผลเป็น 1 row แสดงเป็น tuple

-- (SETOF) — เรียกเหมือน query ตาราง
SELECT * FROM classicmodels.get_customers_by_country('USA');

-- (TABLE) — เรียกเหมือน query ตารางเช่นกัน
SELECT * FROM classicmodels.get_customer_order_summary('USA');
```

---

## การดูโครงสร้าง Table 


```sql
SELECT column_name, data_type
FROM     information_schema.columns
WHERE  table_name = 'customers';

```

---

## RETURN QUERY vs. RETURN NEXT

- `RETURN QUERY` จะ return ข้อมูลมาจาก SQL query โดยตรง
- `RETURN NEXT` ข้อมูลคำนวณ/generate เองด้วย logic (loop, condition)


---

## ตัวอย่าง RETURN NEXT


```sql
CREATE OR REPLACE FUNCTION seqNo(p_limit integer)
RETURNS TABLE (
    seq_no integer,
    created_at timestamp
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_counter integer := 1;
BEGIN
    WHILE v_counter <= p_limit LOOP
        seq_no := v_counter;
        created_at := now();
        RETURN NEXT;  -- ส่ง row ออก 1 แถว
        v_counter := v_counter + 1;
    END LOOP;
    RETURN; -- บอกให้รู้ว่าจบการทำงานแล้ว
END;
$$;

SELECT * FROM seqNo(5);
```

---

## Exercise


ข้อ 1 — View พื้นฐาน

> สร้าง VIEW ชื่อ classicmodels.customerOrderSummary แสดง customerNumber, customerName, และ totalOrders (จำนวน order ทั้งหมดของลูกค้าแต่ละคน)
> - โดย JOIN ระหว่าง customers กับ orders และใช้ GROUP BY 
> - ทดสอบด้วย SELECT * FROM classicmodels.customerOrderSummary ORDER BY totalOrders DESC LIMIT 5;

---

ข้อ 2 — Function (Scalar) ที่ดึงข้อมูลจาก View ในข้อ 1 
> - เขียน FUNCTION ชื่อ classicmodels.get_customer_order_count(p_customerNumber integer) RETURNS integer
> - โดยข้างในให้ SELECT totalOrders INTO ... FROM classicmodels.customerOrderSummary WHERE customerNumber = p_customerNumber;
> - แล้ว RETURN ค่านั้นออกมา (ถ้าไม่พบลูกค้าให้ return 0 แทน NULL) 
> - ทดสอบด้วย SELECT classicmodels.get_customer_order_count(103);

---

ข้อ 3 — Function (RETURNS TABLE) จาก View + WHERE เพิ่มเงื่อนไข
> เขียน FUNCTION ชื่อ classicmodels.get_top_customers(p_min_orders integer) RETURNS TABLE(customerNumber integer, customerName varchar(50), totalOrders bigint) 
> - ที่ RETURN QUERY จาก view ในข้อ 1 กรองเฉพาะลูกค้าที่ totalOrders >= p_min_orders เรียงจากมากไปน้อย 
> - ทดสอบด้วย SELECT * FROM classicmodels.get_top_customers(5);

---

ข้อ 4 — Procedure ที่มี IN/OUT + เรียกใช้ Function จากข้อ 2
> เขียน PROCEDURE ชื่อ classicmodels.check_customer_status(IN p_customerNumber integer, OUT p_status text)
> - โดยข้างในเรียกใช้ classicmodels.get_customer_order_count() จากข้อ 2 มาเก็บในตัวแปร แล้วใช้ IF ตัดสินสถานะ:
>   - 0 order → 'ยังไม่เคยสั่งซื้อ'
>   - 1–4 order → 'ลูกค้าทั่วไป'
>   - 5 ขึ้นไป → 'ลูกค้า VIP'
> - ทดสอบด้วย CALL classicmodels.check_customer_status(103, NULL);

---

ข้อ 5 — Procedure สรุปรายงาน (ผสมทั้ง View + Function + Cursor)

> เขียน PROCEDURE ชื่อ classicmodels.print_vip_report() (ไม่มี parameter)
> - โดยข้างในใช้ cursor วนอ่านข้อมูลจาก classicmodels.get_top_customers(5) (function ในข้อ 3) ทีละแถว 
> - แล้วสำหรับลูกค้าแต่ละคน เรียก classicmodels.check_customer_status() (procedure ในข้อ 4) เพื่อเอาสถานะมา print รวมกันเป็นบรรทัดเดียว เช่น:
>   - ลูกค้า: Baane Mini Imports (103) | จำนวน order: 7 | สถานะ: ลูกค้า VIP
> - ทดสอบด้วย CALL classicmodels.print_vip_report();

---

ข้อ 1

```sql
CREATE OR REPLACE VIEW classicmodels.customerOrderSummary AS 
    SELECT customerNumber, customerName, count(o.orderNumber) as totalOrders      
    FROM orders o 
    INNER JOIN customers USING (customerNumber) 
    GROUP BY customerNumber, customerName;
```

```sql
SELECT customernumber, customername, totalorders
	FROM classicmodels.customerordersummary order by totalOrders desc limit 5;
```

<CsvTable><pre>
"customernumber"	"customername"	"totalorders"
141	"Euro+ Shopping Channel"	26
124	"Mini Gifts Distributors Ltd."	17
114	"Australian Collectors, Co."	5
145	"Danish Wholesale Imports"	5
323	"Down Under Souveniers, Inc"	5
</pre></CsvTable>

---
layout: two-cols
---

::left::

ข้อ 2.

```sql

-- ทดสอบด้วย anonymous block ก่อน

DO $$ LANGUAGE plpgsql

DECLARE
    p_customerNumber integer := 103;
	v_totalOrders integer := 0;
BEGIN
    
    
	select coalesce(max(totalOrders),0) into v_totalOrders 
	from classicmodels.customerOrderSummary
	where customerNumber = p_customerNumber;
	raise notice '%', v_totalOrders;
END;
$$;

```

::right::
```sql

CREATE OR REPLACE FUNCTION 
classicmodels.get_customer_order_count(p_customerNumber integer)
RETURNS integer LANGUAGE plpgsql
AS $$
DECLARE
	v_totalOrders integer;
BEGIN
    
    
	select coalesce(max(totalOrders),0) into v_totalOrders 
	from classicmodels.customerOrderSummary
	where customerNumber = p_customerNumber;
	RETURN v_totalOrders;
END;
$$;
```


<CsvTable><pre>
"get_customer_order_count"
3
</pre></CsvTable>

---

## Error ที่ตรงไหน


```sql

CREATE OR REPLACE FUNCTION 
classicmodels.get_customer_order_count(p_customerNumber integer)
RETURNS integer LANGUAGE plpgsql
AS $$
DECLARE
    p_customerNumber integer;
	v_totalOrders integer;
BEGIN
    
    
	select coalesce(max(totalOrders),0) into v_totalOrders 
	from classicmodels.customerOrderSummary
	where customerNumber = p_customerNumber;
	RETURN v_totalOrders;
END;
$$;
```

<div v-click>ประกาศตัวแปร p_customerNumber ซ้ำ</div>

---
layout: two-cols
---

::left::
ข้อ 3.

```sql
CREATE OR REPLACE FUNCTION 
classicmodels.get_top_customers(p_min_orders integer)
RETURNS TABLE(
    -- classicmodels.customers.customerName%type 
    -- มันจะไปดึงแล้วแปลงเป็น varchar ให้ 
    customerNumber classicmodels
    .customers.customerNumber%TYPE,
    customerName   classicmodels
    .customers.customerName%TYPE,
    totalOrders bigint
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    select c.customerNumber, 
	c.customerName,
	c.totalOrders from 
	classicmodels.customerOrderSummary c
	where c.totalOrders >= p_min_orders
	order by c.totalOrders desc;
END;
$$;
```

::right::

<CsvTable><pre>
"customernumber"	"customername"	"totalorders"
141	"Euro+ Shopping Channel"	26
124	"Mini Gifts Distributors Ltd."	17
148	"Dragon Souveniers, Ltd."	5
323	"Down Under Souveniers, Inc"	5
353	"Reims Collectables"	5
114	"Australian Collectors, Co."	5
145	"Danish Wholesale Imports"	5
</pre></CsvTable>

---
layout: two-cols
---

::left::
ข้อ 4.

```sql
CREATE OR REPLACE PROCEDURE classicmodels.
check_customer_status(IN p_customerNumber integer,
OUT p_status text)
LANGUAGE plpgsql
AS $$
DECLARE
	v_orderCount integer;
BEGIN
    select classicmodels.
	get_customer_order_count(p_customerNumber)
	into v_orderCount;
	
	
		if v_orderCount = 0 then
	  		p_status := 'ยังไม่เคยสั่งซื้อ';
		elsif v_orderCount < 5 then
		    p_status := 'ลูกค้าทั่วไป';
		elsif v_orderCount >=5 then
			p_status := 'ลูกค้า vip';
		else
			p_status := 'Error';
	end if;	
END;
$$;

```

::right::

<CsvTable><pre>
"p_status"
"ลูกค้าทั่วไป"
</pre></CsvTable>

---

ข้อ 5.

```sql
CREATE OR REPLACE PROCEDURE classicmodels.print_vip_report()
LANGUAGE plpgsql AS $$
DECLARE
	c_topCustomer cursor for 
	select * from classicmodels
	.get_top_customers(5);
	v_record record;
	v_status text;
BEGIN
    OPEN c_topCustomer;
	BEGIN
        LOOP
            FETCH c_topCustomer INTO v_record;
            EXIT WHEN NOT FOUND;
			call classicmodels.check_customer_status(v_record.customerNumber, v_status);
            raise notice 'ลูกค้า: %(%)| จำนวน order: %| สถานะ: %', v_record.customerName,
			v_record.customerNumber, v_record.totalOrders, v_status;
        END LOOP;
        CLOSE c_topCustomer;
    EXCEPTION
        WHEN others THEN
            RAISE NOTICE 'Error occurred: %', SQLERRM;            
    END;
END;
$$;
```

---

```
NOTICE:  ลูกค้า: Euro+ Shopping Channel(141)| จำนวน order: 26| สถานะ: ลูกค้า vip
NOTICE:  ลูกค้า: Mini Gifts Distributors Ltd.(124)| จำนวน order: 17| สถานะ: ลูกค้า vip
NOTICE:  ลูกค้า: Dragon Souveniers, Ltd.(148)| จำนวน order: 5| สถานะ: ลูกค้า vip
NOTICE:  ลูกค้า: Down Under Souveniers, Inc(323)| จำนวน order: 5| สถานะ: ลูกค้า vip
NOTICE:  ลูกค้า: Reims Collectables(353)| จำนวน order: 5| สถานะ: ลูกค้า vip
NOTICE:  ลูกค้า: Australian Collectors, Co.(114)| จำนวน order: 5| สถานะ: ลูกค้า vip
NOTICE:  ลูกค้า: Danish Wholesale Imports(145)| จำนวน order: 5| สถานะ: ลูกค้า vip
CALL

Query returned successfully in 118 msec.
```

---
layout: section
---

## การต่อ Database ด้วย Java


---

## Setup - Java for Windows

1. Install Java - https://www.oracle.com/asean/java/technologies/downloads/#java21
2. Create `JAVA_HOME` to `C:\Program Files\Java\jdk-21`
3. Add `C:\Program Files\Java\jdk-21\bin` to `PATH` 

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-03-53-15](/images/2_68_app_sql/2_68_app_sql_2026-02-18-03-53-15.png){.max-h-40vh}
</div>


---

[Download Starter Template]{class="text-2xl"}

1. Goto https://start.spring.io/

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-09-56-59](/images/2_68_app_sql/2_68_app_sql_2026-02-18-09-56-59.png){.max-h-50vh}
</div>

---

2. Extract Zip File
3. Edit pom.xml (DEPENDENCY อื่นไม่เอา)

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-09-59-56](/images/2_68_app_sql/2_68_app_sql_2026-02-18-09-59-56.png){.max-h-50vh}
</div>

---

3. Edit pom.xml

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-10-05-53](/images/2_68_app_sql/2_68_app_sql_2026-02-18-10-05-53.png){.max-h-50vh}
</div>

---
layout: two-cols-title
---

::title::
[4. Edit DemoApplication.java]{class="text-2xl"}

::left::

```java

package pgdemo;

import java.sql.*;

public class App {
    public static void main(String[] args) {
        // PostgreSQL connection parameters
        String url = "jdbc:postgresql://localhost:5432/postgres";
        String username = "postgres";
        String password = "password";
        // In try(....) when error occurred, it will close automatically
        try (Connection conn = DriverManager.getConnection(url, username, password);
             Statement stmt = conn.createStatement(); 
             ResultSet rs = stmt.executeQuery(sql)) {
            System.out.println("Connected to PostgreSQL database!");
            
            
            // Execute query
            String sql = "SELECT * FROM classicmodels.customers LIMIT 5";
            


```

::right::

```java

            // Get metadata
            ResultSetMetaData metadata = rs.getMetaData();
            // Get metadata
            int columnCount = metadata.getColumnCount();
            
            // Print column names
            for (int i = 1; i <= columnCount; i++) {
                System.out.print(metadata.getColumnName(i) + "\t");
            }
            System.out.println("\n" + "-".repeat(50));
            
            // Process results
            while (rs.next()) {
                for (int i = 1; i <= columnCount; i++) {
                    System.out.print(rs.getString(i) + "\t");
                }
                System.out.println();
            }
            
            rs.close();
            stmt.close();
            
        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

::default::


---

[Run App]{class="text-2xl"}

1. Goto folder demo

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-10-12-28](/images/2_68_app_sql/2_68_app_sql_2026-02-18-10-12-28.png){.max-h-40vh}
</div>

---

2. Open powershell `.\mvnw clean compile exec:java`

<div class="w-fit mx-auto">

![2_68_app_sql_2026-02-18-10-10-58](/images/2_68_app_sql/2_68_app_sql_2026-02-18-10-10-58.png){.max-h-45vh}
</div>