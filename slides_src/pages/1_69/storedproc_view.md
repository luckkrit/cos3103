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
layout: two-cols-header
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
layout: two-cols-header
---

# Example 1

::left::
```sql
CREATE VIEW salePerOrder AS
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
layout: two-cols
---

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
