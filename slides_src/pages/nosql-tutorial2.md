---
title: NoSQL - Tutorial2
transition: fade
---

# NoSQL Tutorial2

---

## What is Aggregation?

- Aggregation is like a data processing pipeline - you put documents in one end, and they get transformed step by step until you get the results you want.

<div class="w-[700px] mx-auto">

![Aggregation Pipeline](https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F2809lspwb4ah36t87e2r.jpg)

</div>

```python

db.collection.aggregate( [ { <stage> }, ... ] )

```

---

# Example 1:

- Find products where productLine is Motorcycles and buyPrice is less than 60

- Using `find`

```python
execute(lambda client: find(client.classic.products.find({"product.Line":"Motorcycles","buyPrice":{"$lt":60}})))
```

- Using aggregate
    - `{ $match: { <query predicate> } }`

```python
execute(lambda client: aggregate(client.classic.products.aggregate([{"$match":{"product.Line":"Motorcycles","buyPrice":{"$lt":60}}}])))
```

---

# Questions

1. Find customer who has credit limit less than 50000 and greater than 20000
2. Find customer whose contact city is Nantes
3. Find employees whose last name is Patterson

---

# Example 2:

- Find product name, buyPrice, productLine where productLine is Motorcycles and buyPrice is less than 60

- Using aggregate
    - `{ $match: { <query predicate> } }`
    - `{ $project: { <specification(s)> } }`


```python
pipelines = []
pipelines.append({"$match":{"product.Line":"Motorcycles","buyPrice":{"$lt":60}}})
pipelines.append({"$project":{"product.Name":True,"buyPrice":True,"product.Line":True, "_id": False}})
execute(lambda client: aggregate(client.classic.products.aggregate(pipelines)))
```

---

# Questions

1. Find customer number, name, contact firstname contact lastname
2. Find office code, city, country, postal code
3. Find product in stock, buy price, name, code and line

---

# Example 3:

- Find the 3 cheapest motorcycles under $60 and show me their name, price, and category

- Using aggregate
    - `{ $match: { <query predicate> } }`
    - `{ $project: { <specification(s)> } }`
    - `{ $sort: { <field1>: <sort order>, <field2>: <sort order> ... } }`
    - `{ $limit: <positive 64-bit integer> }`

```python
pipelines = []
pipelines.append({"$match":{"product.Line":"Motorcycles","buyPrice":{"$lt":60}}})
pipelines.append({"$project":{"product.Name":True,"buyPrice":True,"product.Line":True, "_id": False}})
pipelines.append({"$sort":{"buyPrice":1}})
pipelines.append({"$limit":3})
execute(lambda client: aggregate(client.classic.products.aggregate(pipelines)))
```

---

# Questions

1. List the name, number, and sales employee number of the top 5 customers with the highest credit limit
2. List 3 customers number and name who have not contact sales

---

# Example 4:

- Find product code, name, price, category and quantity order

- Using aggregate
    - `{ $lookup:{...}}`
    - `{ $project: { <specification(s)> } }`

```javascript
{
    $lookup:{
       from: <collection to join>,
       localField: <field from the input documents>,
       foreignField: <field from the documents of the "from" collection>,
       let: { <var_1>: <expression>, …, <var_n>: <expression> },
       pipeline: [ <pipeline to run> ],
       as: <output array field>
    }
}
```

---

```python

pipelines = []
pipelines.append({"$lookup":{"from": "products",
  "localField": "productCode",
  "foreignField": "product.Code",
  "as": "product_order"}})
pipelines.append(
{
    "$project":{
        "productCode": 1,
  "quantityOrdered": 1,
  "product_order.product.Name": 1,
  "product_order.buyPrice": 1,
  "product_order.Line": 1,
  "_id": 0
}
}
)
execute(lambda client: aggregate(client.classic.orderdetails.aggregate(pipelines)))
```

==$lookup returns an array (product_order), even if there's only one match.==

```bash
{'productCode': 'S32_1268', 'quantityOrdered': 1, 'product_order': [{'buyPrice': Decimal128('53.93'), 'product': {'Name': '1980’s GM Manhattan Express'}}]}
```

- Flatten result?

---

# Example 5:

- using `$unwind` to destruct array of product_order from previous example

- Using aggregate
    - `{ $lookup:{...}}`
    - `{ $unwind: <field path> }`
    - `{ $project: { <specification(s)> } }`

---

```python

pipelines = []
pipelines.append({"$lookup":{"from": "products",
  "localField": "productCode",
  "foreignField": "product.Code",
  "as": "product_order"}})
pipelines.append({"$unwind":"$product_order"})
pipelines.append(
{
    "$project":{
        "productCode": 1,
  "quantityOrdered": 1,
  "product_order.product.Name": 1,
  "product_order.buyPrice": 1,
  "product_order.Line": 1,
  "_id": 0
}
}
)
execute(lambda client: aggregate(client.classic.orderdetails.aggregate(pipelines)))
```

**OUTPUT - From 1 document**

```bash
{'productCode': 'S32_1268', 'quantityOrdered': 1, 'product_order': {'buyPrice': Decimal128('53.93'), 'product': {'Name': '1980’s GM Manhattan Express'}}}
```

---

# Example 6:

- using `$addFields` - Adds new fields to documents. 

- To flatten result, remove embeded object

- Using aggregate
    - `{ $lookup:{...}}`
    - `{ $unwind: <field path> }`
    - `{ $addFields: { <newField>: <expression>, ... } }`
    - `{ $project: { <specification(s)> } }`

---

```python
pipelines = []
pipelines.append({"$lookup":{"from": "products",
  "localField": "productCode",
  "foreignField": "product.Code",
  "as": "product_order"}})
pipelines.append({"$unwind":"$product_order"})
pipelines.append({ "$addFields": { 
        "productName": "$product_order.product.Name",
        "buyPrice": "$product_order.buyPrice",
        "Line": "$product_order.Line"
    } })
pipelines.append(
{
    "$project":{
        "_id": 0,
        "productCode": 1,
        "quantityOrdered": 1,
        "productName": 1,
        "buyPrice": 1,
        "Line": 1
}})
execute(lambda client: aggregate(client.classic.orderdetails.aggregate(pipelines)))
```

**OUTPUT - From 1 document**

```bash
{'productCode': 'S18_1749', 'quantityOrdered': 30, 'productName': '1917 Grand Touring Sedan', 'buyPrice': Decimal128('86.70')}
```

---

# Example 7:

- Find product name and code from order that status is Shipped for 5 documents first then order by product code

- Using aggregate
    - `{ $lookup:{...}}`
    - `{ $match: { <query predicate> } }`
    - `{ $unwind: <field path> }`
    - `{ $addFields: { <newField>: <expression>, ... } }`
    - `{ $project: { <specification(s)> } }`
    - `{ $limit: <positive 64-bit integer> }`
    - `{ $sort: { <field1>: <sort order>, <field2>: <sort order> ... } }`

---

```python

embedded_pl = [{"$match": {"$expr": {"$eq": ["$product.Code", "$$productCode"]}  }}]
pipelines = []
pipelines.append({"$lookup":{"from": "products","let": {"productCode": "$productCode",},"pipeline": embedded_pl,
"as": "product_orders"}})
embedded_pl2 = [{"$match": {"$expr": {"$eq": ["$orderNumber", "$$o_no"]}}}]
pipelines.append({"$lookup":{"from": "orders","let":{"o_no": "$orderNumber"},"pipeline": embedded_pl2,"as": "order_details"}})
pipelines.append({"$unwind":"$product_orders"})
pipelines.append({"$unwind":"$order_details"})
pipelines.append({"$match":{"order_details.status":{"$eq":"Shipped"}}})
pipelines.append({ "$addFields": { "productName": "$product_orders.product.Name","productCode": "$product_orders.product.Code",
"orderStatus": "$order_details.status",} })
pipelines.append({"$project":{"_id": 0, "productCode": 1,"productName": 1,"orderStatus": 1,}})
pipelines.append({
    "$limit": 5
})
pipelines.append({
    "$sort": {"productCode":1}
})
execute(lambda client: aggregate(client.classic.orderdetails.aggregate(pipelines)))
```

- What happend if sort before limit?

---

# Example 8:

- `SELECT COUNT(*) AS count FROM orders`

- using aggregate `$group` and `$sum`

```python

pipelines = []
pipelines.append({
    "$group":{
        "_id": None,  # grouping all documents into a single group
        "count":{"$sum": 1}
    }
})
execute(lambda client: aggregate(client.classic.orders.aggregate(pipelines)))
```

- using aggreate `$count`

```python

pipelines = []
pipelines.append({
        '$count': 'count'
    })
execute(lambda client: aggregate(client.classic.orders.aggregate(pipelines)))
```

---

# Example 9:

- `SELECT SUM(priceEach * quantityOrdered) AS total FROM orderdetails`

- using aggregate `$group` , `$sum`, `$multiply`

```python
pipelines = []
pipelines.append({
    "$group":{
        "_id": None,
        "total":{"$sum": {"$multiply":["$priceEach", "$quantityOrdered"]}}
    }
})
execute(lambda client: aggregate(client.classic.orderdetails.aggregate(pipelines)))
```

- 9604241.11

---

# Example 10:

- `select o.customerNumber, sum(d.quantityOrdered * d.priceEach) as total from orders o left join orderdetails d on o.orderNumber = d.orderNumber group by o.customerNumber having total < 50000`

- using aggregate `$group` , `$sum`, `$multiply`, `$lookup`, `$match`

```python
embedded_pl = [{"$match": {"$expr": {"$eq": ["$orderNumber", "$$o_no"]}}}]
pipelines = []
pipelines.append({"$lookup":{"from": "orders","let":{"o_no":"$orderNumber"},"pipeline": embedded_pl,"as": "order_details"}})
pipelines.append({"$unwind":"$order_details"})
pipelines.append({ "$addFields": { "customerNumber": "$order_details.customerNumber",} })
pipelines.append({"$group":{"_id": "$customerNumber","total":{"$sum": {"$multiply":["$priceEach", "$quantityOrdered"]}}}})
pipelines.append({
    "$match":{
        "total":{"$lt":50000}
    }
})
pipelines.append({"$sort":{"_id":1}})
# pipelines.append({"$count":"total"})
execute(lambda client: aggregate(client.classic.orderdetails.aggregate(pipelines)))
```

---

- For more reference: https://www.mongodb.com/docs/manual/reference/sql-aggregation-comparison/

---

# Excercise

🟢 Beginner Level (Basic Aggregation)
1. Grouping & Counting
    - Count how many products are in each product line
    - Count total number of orders per customer
    - Find how many employees work in each office
2. Simple Calculations
    - Calculate the total value of all products in stock (quantityInStock × buyPrice)
    - Find the average order value (priceEach × quantityOrdered) per order
    - Calculate total sales amount for each product

---

3. Filtering & Sorting
    - Find the top 5 most expensive products by MSRP
    - Show customers who have placed more than 5 orders
    - List products with stock quantity less than 1000, sorted by quantity

🟡 Intermediate Level (Joins & Complex Logic)

4. Single Lookup

    - Join orderdetails with products to show product names alongside order information
    - Join orders with customers to display customer names for each order
    - Join employees with offices to show office city and country for each employee
---


5. Multiple Lookups

    - Show order details with product information AND customer information (2 lookups)
    - Display employees with their office details AND their manager's name (2 lookups)
    - Get orderdetails with product info, order info, and customer info (3 lookups)

6. Aggregation with Filtering

    - Find total sales amount per product line (join orderdetails with products, then group)
    - Calculate average order value per customer (must join orders with orderdetails)
    - Show which sales representatives have the highest total sales