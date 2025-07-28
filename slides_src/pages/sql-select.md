---
title: SQL - SELECT
transition: fade
---

# SQL - SELECT

---

# DOWNLOAD SCHEMA & DATA

[DOWNLOAD SCHEMA & DATA](https://luckkrit.github.io/cos3103/sql/mysqlsampledatabase-classicmodels.sql)

---
layout: section
---

# IS NULL OPERATOR

---
layout: two-cols
---

# IS NULL Operator

1. If the value is NULL, the expression returns true. Otherwise, it returns false. 
2. Cannot use equality (=) comparison to check for null values

- กรณี salesRepEmployeeNumber IS NULL

```sql
SELECT customerName, country, salesRepEmployeeNumber 
FROM customers 
WHERE salesRepEmployeeNumber IS NULL; 
```

- กรณี salesRepEmployeeNumber IS NOT NULL

```sql
SELECT customerName, country, salesRepEmployeeNumber 
FROM  customers 
WHERE salesRepEmployeeNumber IS NOT NULL; 
```

::right::

<div class="w-[300px] mx-auto">

![CUSTOMER](/images/sql_select/customers.png)
</div>

---
layout: section
---

# Arithmetic Expression

---

# BETWEEN

```sql
SELECT * 
FROM classicmodels.orderdetails
where priceEach between 150 and 200
```

![BETWEEN](/images/sql_select/between.png)

---

- 2 SQL นี้ให้ผลลัพธ์เหมือนกัน

- อันที่ 1
```sql
SELECT quantityOrdered , 
              priceEach ,  
             (priceEach*quantityOrdered)-(priceEach*quantityOrdered)*0.1 
FROM  classicmodels.orderdetails
where  (priceEach*quantityOrdered) < 800 and
            (priceEach*quantityOrdered) > 700 ;
```

- อันที่ 2
```sql
SELECT quantityOrdered , 
              priceEach ,  
             (priceEach*quantityOrdered) * 0.9
FROM  classicmodels.orderdetails
where  (priceEach*quantityOrdered) < 800 and
            (priceEach*quantityOrdered) > 700 ;
```

---

- เขียนให้เข้าใจง่ายขึ้น
```sql
SELECT quantityOrdered , 
              priceEach ,  
             quantityOrdered,
             (priceEach * quantityOrdered) as total_price,
             (priceEach * quantityOrdered) * 0.9 as discounted_price
FROM  classicmodels.orderdetails
where  (priceEach*quantityOrdered) < 800 and
            (priceEach*quantityOrdered) > 700 ;
```

---
layout: section
---

# Aggregate Function

---

# AVG - FUNCTION AVERAGE

- จากตัวอย่างที่แล้ว ถ้าจะคำนวณค่าเฉลี่ยของราคา

```sql
SELECT quantityOrdered , 
       priceEach
             -- ,avg(priceEach) as avgPrice
FROM  classicmodels.orderdetails
where  (priceEach*quantityOrdered) < 800 and
            (priceEach*quantityOrdered) > 700 ;

```

- ถ้าเราทำการ uncomment ออกจะเกิดอะไรขึ้น

```sql

SELECT quantityOrdered , 
       priceEach
             ,avg(priceEach) as avgPrice
FROM  classicmodels.orderdetails
where  (priceEach*quantityOrdered) < 800 and
            (priceEach*quantityOrdered) > 700 ;
```

---

- มันจะแสดงบรรทัดเดียว เพราะว่า

1. AVG(priceEach) is an aggregate function, which summarizes all rows into a single value.

"Aggregate = การรวมข้อมูลหลายแถวให้เป็นค่าผลลัพธ์เดียว"

2. But you're also selecting quantityOrdered and priceEach, which are non-aggregated columns.

3. Most databases will return an error like "not a GROUP BY expression", but some SQL engines (e.g., MySQL in certain modes) may just return 1 row with arbitrary values for non-aggregated columns and the correct AVG.

- เราจะพูดถึง GROUP BY ในภายหลัง
- ดังนั้น Aggregate ฟังก์ชั่นจะประกอบด้วย MIN, MAX, COUNT, SUM, AVG

---

- ผลลัพธ์ของ AVG คือค่าเฉลี่ย

|quantityOrdered|priceEach|
|---------------|---------|
|22             |36.29    |
|22             |33.19    |
|20             |39.80    |
|20             |39.02    |

- วิธีที่ 1

```sql
SELECT avg(priceEach) as avgPrice
FROM  classicmodels.orderdetails
where  (priceEach*quantityOrdered) < 800 and
            (priceEach*quantityOrdered) > 700 ;
```

- วิธีที่ 2

```sql
SELECT (36.29+33.19+39.80+39.02)/4 as avgPrice
```
---

# SUM

```sql
SELECT SUM(priceEach) as totalPrice
FROM  classicmodels.orderdetails
where  (priceEach*quantityOrdered) < 800 and
            (priceEach*quantityOrdered) > 700 ;
```

- ผลลัพธ์ที่ได้คือ 148.30

---

# MIN

```sql
SELECT MIN(priceEach) as minPrice
FROM  classicmodels.orderdetails
where  (priceEach*quantityOrdered) < 800 and
            (priceEach*quantityOrdered) > 700 ;
```

- ผลลัพธ์ที่ได้คือ 33.19

---

# MAX

```sql
SELECT MAX(priceEach) as maxPrice
FROM  classicmodels.orderdetails
where  (priceEach*quantityOrdered) < 800 and
            (priceEach*quantityOrdered) > 700 ;
```

- ผลลัพธ์ที่ได้คือ 39.80



---

# COUNT Function

- นับจำนวนแถว

```sql

SELECT  
        count(*)
FROM    classicmodels.customers
```

- แล้วถ้าเป็นแบบนี้

```sql
SELECT  
        count(salesRepEmployeeNumber)
FROM    classicmodels.customers

```

- ผลลัพธ์ที่ได้จำนวนไม่เท่ากัน เพราะว่า COUNT(*) includes NULLs, but COUNT(column) does not.

---

# IF Function

- จากตัวอย่างก่อนหน้าสามารถเขียนโดยใช้ IF ช่วยได้

- IF(condition, ถ้าจริง return อะไร, ถ้าเท็จ return อะไร)

    
```sql
SELECT COUNT(IF(salesRepEmployeeNumber IS NULL, 1, 1)) AS null_count
FROM classicmodels.customers;

```

- จากกรณีนี้ ถ้า salesRepEmployeeNumber IS NULL ก็ให้คืนค่า 1 ถ้าไม่ใช่ ก็คือให้คืนค่า 1



---
layout: section
---

# IN OPERATOR

---
layout: two-cols
---

# IN OPERATOR

- Query: Retrieve the contact of all employees who work on salesRepEmployeeNumber 1370, 1501, or 1504 

```sql
SELECT contactLastName,   
        salesRepEmployeeNumber
FROM    classicmodels.customers
where   salesRepEmployeeNumber 
			in (1370 ,1501 ,1504 )
```

::right::

![IN OPERATOR](/images/sql_select/in_operator.png)


---

# NOT IN OPERATOR

- Query: Retrieve the contact of all employees who not work on salesRepEmployeeNumber 1370, 1501, or 1504

```sql
SELECT contactLastName,   
        salesRepEmployeeNumber
FROM    classicmodels.customers
where   salesRepEmployeeNumber 
        not in (1370 ,1501 ,1504 )
```

- ให้ผลลัพธ์ที่ตรงข้ามกัน

![NOT IN OPERATOR](/images/sql_select/not_in_operator.png)

- จากรูปข้างบน ถ้า 2 จำนวนมาบวกกันจะได้ 100 แถว แล้วถ้าเลือกข้อมูลทั้งหมดออกมา จะมีกี่แถว?

<div v-click>

![SELECT ALL](/images/sql_select/select_all.png)
</div>

- อีก 22 แถวคือแถวที่มี salesRepEmployeeNumber เป็น NULL ดังนั้น NOT IN ไม่ได้รวม NULL ไปด้วย

---

- ถ้าต้องการให้รวมแถวที่มี salesRepEmployeeNumber ที่เป็น NULL ไปด้วยควรจะทำยังไง

````md magic-move
```sql {*}
SELECT contactLastName,   
        salesRepEmployeeNumber
FROM    classicmodels.customers
where   salesRepEmployeeNumber 
        not in (1370 ,1501 ,1504 ) 
```

```sql {5}
SELECT contactLastName,   
        salesRepEmployeeNumber
FROM    classicmodels.customers
where   salesRepEmployeeNumber 
        not in (1370 ,1501 ,1504, NULL )
```

```sql {5}
SELECT contactLastName,   
        salesRepEmployeeNumber
FROM    classicmodels.customers
where   salesRepEmployeeNumber 
        not in (1370 ,1501 ,1504 ) OR salesRepEmployeeNumber IS NULL
```

````

---

- จากตัวอย่างก่อนหน้า ใน IN (1370, 1501, 1504, NULL) จะไม่แสดงผลลัพธ์อะไรออกมา เพราะ SQL ไม่รู้จะเปรียบเทียบ NULL ยังไง

---

IN กับ OR สามารถเขียนให้ผลลัพธ์ได้เหมือนกัน

- ตัวอย่างที่ 1
```sql

SELECT contactLastName,   
        salesRepEmployeeNumber
FROM    classicmodels.customers
where   salesRepEmployeeNumber 
        in (1370 ,1501 ,1504 ) 

```

- ตัวอย่างที่ 2

```sql

SELECT contactLastName,   
        salesRepEmployeeNumber
FROM    classicmodels.customers
where   salesRepEmployeeNumber = 1370 or salesRepEmployeeNumber = 1501 or salesRepEmployeeNumber = 1504 

```
