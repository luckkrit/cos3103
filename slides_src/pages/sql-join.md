

<!-- 
---
layout: section
---

# Cartesian Products

---

# FROM Clause (Multiple Tables)

```sql
SELECT 	<attribute list>
	FROM 	<table list>

```

- Table list may include
    - Names of 1 or more tables
    - Subquery for joined tables

---
layout: two-cols
---

# จากการดึงค่า 2 ตาราง

- ตัวอย่างที่ 1

```sql
SELECT * FROM classicmodels.offices;

```

![SELECT * FROM OFFICES](/images/sql_select/select_offices.png)

::right::

# &nbsp;

- ตัวอย่างที่ 2

```sql

SELECT * FROM classicmodels.productlines;
```

![SELECT * FROM PRODUCTLINES](/images/sql_select/select_productlines.png)

---

- ถ้าเขียนแบบนี้

```sql
SELECT *  FROM offices , productlines
```

![SELECT * FROM OFFICES,PRODUCTLINES](/images/sql_select/select_offices_productlines.png)

- จะได้ 7 x 7 = 49 rows และมีการซ้ำกัน

![49 rows](/images/sql_select/total_rows_offices_productlines.png)

---

- ถ้าจะให้อธิบายการทำงานในลักษณะ Coding

![Cartesian vs Coding](/images/sql_select/cartesian_coding.png)

---
layout: section
---

# JOIN

---

# Cartesian R x S

- ถ้ามีตาราง R x S

<div class="w-[400px]">

![Cartesian R x S](/images/sql_select/cartesian_r_x_s.png)
</div>

- สมการ Relational Algebra

<div class="w-[400px]">

![SELECT (R x S)](/images/sql_select/algebra_select_cartesian.png)
</div>

---

# FROM 

- สมการ Relational Algebra

<div class="w-[400px]">

![JOIN (R x S)](/images/sql_select/algebra_select_cartesian2.png)
</div>

- SQL ที่ได้จะเป็นดังรูป

<div class="w-[400px]">

![SQL JOIN](/images/sql_select/sql_join.png)
</div>

---

# FROM

- OUTPUT

<div class="w-[400px]">

![SQL JOIN](/images/sql_select/join_output.png)
</div>

---
layout: two-cols
---

# FROM

- จากรูป ถ้าเราใช้ FROM มากกว่า 2 ตาราง เราตีความได้ว่า Finding all order details of  each order
```sql
select  r.orderNumber, s.orderNumber, 
            r.customerNumber, r.orderDate ,
            s.productCode, s.quantityOrdered 
from   orders as r , orderdetails as s
where r.orderNumber =  s.orderNumber
```


::right::

<div class="w-[150px] mx-auto">

![ORDER DETAILS VS. ORDER](/images/sql_select/orderdetails_orders.png)
</div> -->