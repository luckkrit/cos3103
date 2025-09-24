---
title: NoSQL - Tutorial
transition: fade
---

# NoSQL Tutorial

---

# PyMongo

## PEP 249 - Python Database API Specification 2.0 ⚠️ (Partial)
- PyMongo does NOT fully follow PEP 249 because:

    1. MongoDB is NoSQL, not SQL
    2. Uses its own API design (find, insert_one, etc.)
    3. But it does follow: connection, cursor concepts

---

# Setup MongoDB & Migration tools

- Setup MongoDB https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-8.0.13-signed.msi

- Download MySQL Connector/J 9.4.0 https://dev.mysql.com/downloads/connector/j/

- MongoDB Relational Migrator https://www.mongodb.com/try/download/relational-migrator

- Migrate classicmodels in MySQL to MongoDB

---

# Install PyMongo

```bash
pip install pymongo
```


---

# Collections

- Like table in SQL

```python

from pymongo import MongoClient
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
try:
    db = client['classic']
    customers = db.customers # collection customers
    orders = db.orders # collection orders
    products = db.products # collection products
    orderdetails = db.orderdetails # collection orderdetails
    client.close()
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)

```

---

# What does collections hold?

- Customers who place orders
- Products (model cars) organized by product lines
- Orders containing multiple products
- Employees who manage customer relationships

```python
# In SQL, you'd have separate tables
customers_table = "id, name, address, phone"
orders_table = "id, customer_id, date, status"  
order_items_table = "order_id, product_id, quantity, price"
```

---

# What does collections hold?

```python
# A customer document can contain related information
customer_doc = {
    "customerNumber": 103,
    "name": "Atelier graphique",
    "contact": {
        "firstName": "Carine",
        "lastName": "Schmitt",
        "phone": "40.32.2555"
    },
    "address": {
        "street": "54, rue Royale",
        "city": "Nantes", 
        "country": "France",
        "postalCode": "44000"
    },
    "creditLimit": 21000,
    "salesRep": {
        "employeeNumber": 1370,
        "name": "Gerard Hernandez"
    }
}
```

---
layout: two-cols
---

# Advantages

1. Natural Data Grouping

```python


customer_doc = {
    "customerNumber": 103,
    "name": "Atelier graphique",
    "contact": {
        "firstName": "Carine",
        "lastName": "Schmitt",
        "phone": "40.32.2555"
    },
    "address": {
        "street": "54, rue Royale",
        "city": "Nantes", 
        "country": "France",
        "postalCode": "44000"
    },
    "creditLimit": 21000,
    "salesRep": {
        "employeeNumber": 1370,
        "name": "Gerard Hernandez"
    }
}


```

::right::

```python
# Address isn't a separate table - it's part of the 
# customer

# Easy navigation
customer_city = customer_doc["address"]["city"]          

# Intuitive structure
customer_name = customer_doc["contact"]["firstName"]     

print(customer_city, customer_name)
```

---

# Advantages

2. Flexible Schema

```python

# Some customers might have different fields
corporate_customer = {
    "customerNumber": 104,
    "name": "Signal Gift Stores",
    # No individual contact person
    "address": {"street": "8489 Strong St.", "city": "Las Vegas"},
    # Has special corporate fields
    "corporateDiscount": 0.15,
    "paymentTerms": "Net 30"
}

```

---

# Advantages

3. Arrays for Multiple Values

```python

# Customer can have multiple phone numbers
multi_contact_customer = {
    "customerNumber": 105,
    "name": "La Rochelle Gifts", 
    "phones": [
        {"type": "office", "number": "40.67.8555"},
        {"type": "mobile", "number": "40.67.8556"}
    ]
}

```

---

# Creating collections and documents

- Insert one ducment to customers2 (created automatically) 

```python
# Insert a customer (collection created automatically)
customer = {
    "customerNumber": 103,
    "name": "Atelier graphique",
    "contact": {
        "firstName": "Carine",
        "lastName": "Schmitt",
        "phone": "40.32.2555"
    },
    "address": {
        "street": "54, rue Royale",
        "city": "Nantes",
        "country": "France", 
        "postalCode": "44000"
    },
    "creditLimit": 21000
}

# Insert one customer
result = customers.insert_one(customer)
print(f"Inserted customer with ID: {result.inserted_id}")
```

---
layout: two-cols
---

# Creating collections and documents

- Insert multiple documents to customers2

```python
# Insert multiple customers
customer_list = [
    {
        "customerNumber": 112,
        "name": "Signal Gift Stores",
        "address": {
            "street": "8489 Strong St.",
            "city": "Las Vegas",
            "country": "USA",
            "postalCode": "83030"
        },
        "creditLimit": 71800
    },
```
::right::

```python

    {
        "customerNumber": 114, 
        "name": "Australian Collectors, Co.",
        "contact": {
            "firstName": "Peter",
            "lastName": "Ferguson"
        },
        "address": {
            "street": "636 St Kilda Road",
            "city": "Melbourne",
            "country": "Australia", 
            "postalCode": "3004"
        },
        "creditLimit": 117300
    }
]

result = customers.insert_many(customer_list)
print(f"Inserted {len(result.inserted_ids)} customers")
```

---

# Finding Documents

- Find all customers from collections customers2

```python
# Find all customers
all_customers = customers.find()
for customer in all_customers:
    pprint(customer)
```

- Find customers in France

```python

# Find customers in France
french_customers = customers.find({"address.country": "France"})
for customer in french_customers:
    print(f"{customer['name']} - {customer['address']['city']}")

```

---

# Exercise

- From collection customers

1. Find customer by customerNumber is 103
2. Find customers where state is NULL
3. Find customers where city is San Francisco
4. Find customers where postalCode is 97562 
5. Find customers where salesRepEmployeeNumber is '1166' or 1166. Which one gets results?

---

# Finding Documents (cont.)

- Find customers with high credit limits from collection customers2

```python
# Find customers with high credit limits
high_credit = customers.find({"creditLimit": {"$gt": 100000}})
print(f"High credit customers: {high_credit.count()}")
```

- Find by nested field from collection customers2

```python
# Find by nested field
peters = customers.find({"contact.firstName": "Peter"})
for peter in peters:
    print(f"Found Peter: {peter['name']}")
```

- Multiple conditions from collection customers2

```python
# Multiple conditions (AND)
usa_high_credit = customers.find({
    "address.country": "USA",
    "creditLimit": {"$gt": 50000}
})

print("USA customers with high credit:")
for customer in usa_high_credit:
    print(f"- {customer['name']}: ${customer['creditLimit']:,}")
```

---

# Finding Documents (cont.)

- Comparison operators

```python

# Comparison operators
high_credit = customers.find({"creditLimit": {"$gt": 50000}})     # Greater than
very_high_credit = customers.find({"creditLimit": {"$gte": 50000}})    # Greater than or equal
low_credit = customers.find({"creditLimit": {"$lt": 100000}})    # Less than
max_credit = customers.find({"creditLimit": {"$lte": 100000}})   # Less than or equal
not_50k = customers.find({"creditLimit": {"$ne": 50000}})     # Not equal

```

- In operator from collection customers2

```python
# IN operator
target_countries = customers.find({
    "address.country": {"$in": ["USA", "France", "Australia"]}
})
```

---

# Finding Documents (cont.)

- Or operator from collection customers2

```python
# OR conditions
usa_or_rich = customers.find({
    "$or": [
        {"address.country": "USA"},
        {"creditLimit": {"$gt": 100000}}
    ]
})
```

- Field exists from collection customers2

```python
# Field exists
has_contact = customers.find({"contact.firstName": {"$exists": True}})


```

---

# Finding Documents (cont.)

- Matching with regular expression

```python
# Pattern matching (regex)
gift_stores = customers.find({"name": {"$regex": "Gift", "$options": "i"}})  # Case insensitive

# Print results with count
print(f"Gift stores found: {gift_stores.count()}")
for store in gift_stores:
    print(f"- {store['name']}")
```

---

# Exercise

- From collection customers2

1. Find customers where creditLimit is between 50,000 and 100,000
2. Find customers who are in USA and France whose creditLimit is between 10,000 and 80,000 
3. Find customers whose creditLimit is less than 100,000

---

# Projection - Selecting Fields

- Show only name and country

```python
# Show only name and country
name_country = customers.find(
    {"address.country": "USA"},
    {"name": 1, "address.country": 1, "_id": 0}
)

print("USA Customers:")
for customer in name_country:
    print(f"- {customer['name']} in {customer['address']['country']}")

```

- Exclude specific fields

```python
# Exclude specific fields
no_contact = customers.find({}, {"contact": 0, "_id": 0})

```

- Clean display

```python
# Create a clean display
usa_customers = customers.find(
    {"address.country": "USA"},
    { "name": 1, "city": "$address.city", "creditLimit": 1, "_id": 0 }
)
```

---

# Projection - Selecting Fields (cont.)

- Convert to list for reuse after loop and not suitable for large datasets to avoid memory crash

```python
# Create a clean display
usa_customers = customers.find(
    {"address.country": "USA"},
    { "name": 1, "city": "$address.city", "creditLimit": 1, "_id": 0 }
)
print(type(usa_customers)) #<class 'pymongo.synchronous.cursor.Cursor'>
# Convert to list for easier handling
usa_list = list(usa_customers)
for customer in usa_list:
    print(f"{customer['name']} - Credit: ${customer['creditLimit']:,}")
```

---
layout: two-cols
---

# collection products2

```python
# Insert products with rich document structure
product_list = [
    {
        "productCode": "S18_1749",
        "name": "1917 Grand Touring Sedan", 
        "description": "This 1:18 scale replica of the 1917 Grand Touring car...",
        "productLine": "Vintage Cars",
        "scale": "1:18",
        "vendor": "Welly Diecast Productions",
        "quantityInStock": 2724,
        "pricing": {
            "buyPrice": 86.70,
            "MSRP": 170.00,
            "margin": 83.30
        },
        "specifications": {
            "weight": "1.5 lbs",
            "dimensions": {
                "length": "10 inches",
                "width": "4 inches", 
                "height": "3 inches"
            }
        }
    },

```

::right::


```python

    {
        "productCode": "S18_2248",
        "name": "1911 Ford Town Car",
        "description": "Features opening hood, opening doors, opening trunk...",
        "productLine": "Vintage Cars", 
        "scale": "1:18",
        "vendor": "Motor City Art Classics",
        "quantityInStock": 540,
        "pricing": {
            "buyPrice": 33.30,
            "MSRP": 60.54,
            "margin": 27.24
        }
    }
]

# Insert products
result = products.insert_many(product_list)
print(f"Inserted {len(result.inserted_ids)} products")
```

---

# Querying Products from collection products2

- Find vintage cars

```python
# Find vintage cars
vintage_cars = products.find({"productLine": "Vintage Cars"})
print("Vintage Cars:")
for car in vintage_cars:
    print(f"- {car['name']} (Stock: {car['quantityInStock']})")
```

- Find products with low stock

```python
# Find products with low stock
count_low_stock = products.count_documents({"quantityInStock": {"$lt": 1000}})
print(f"\nLow stock products: {count_low_stock}")
```

- Find by price ranage

```python
# Find by price range
affordable_products = products.find({
    "pricing.MSRP": {"$gte": 50, "$lte": 100}
})
print("\nAffordable products ($50-$100):")
for product in affordable_products:
    price = product['pricing']['MSRP']
    print(f"- {product['name']}: ${price}")

```

---

# Querying Products (cont.)

- Find by vendor

```python
# Find by vendor (case insensitive)
motor_city_products = products.find({
    "vendor": {"$regex": "Motor City", "$options": "i"}
})

# Complex query with multiple conditions
count_premium_vintage = products.count_documents({
    "productLine": "Vintage Cars",
    "quantityInStock": {"$gt": 500},
    "pricing.MSRP": {"$lt": 100}
})

print(f"\nPremium vintage cars in stock: {count_premium_vintage}")
```

---

# Sorting

- ascending

```python
# Sort by credit limit (ascending)
customers_asc = customers.find().sort("creditLimit", 1)
print("Customers by credit limit (ascending):")
for customer in customers_asc.limit(3):
    print(f"- {customer['name']}: ${customer['creditLimit']:,}")
```

- descending

```python
# Sort by credit limit (descending)  
customers_desc = customers.find().sort("creditLimit", -1)
print("\nTop 3 customers by credit limit:")
for customer in customers_desc.limit(3):
    print(f"- {customer['name']}: ${customer['creditLimit']:,}")
```

- multiple fields

```python
# Sort by multiple fields
multi_sort = customers.find().sort([
    ("address.country", 1),
    ("creditLimit", -1)
])
```

---

# Sorting (cont.)

- Skip and Limit

```python
# Skip and limit (pagination)
skip = 1
limit = 3
page_2 = customers.find().skip(skip).limit(limit)
print(f"\nPage 2 customers ({skip}-{limit}):")
for i, customer in enumerate(page_2, skip):
    print(f"{i}. {customer['name']}")
```

---

# Basic Aggregation Introduction
## What is Aggregation?
- Aggregation is like a data processing pipeline - you put documents in one end, and they get transformed step by step until you get the results you want.

![Aggregation Pipeline](https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F2809lspwb4ah36t87e2r.jpg)

---

# Optimal Stages Ordering

```javascript
[
  {"$match": {...}},    // 1. Filter FIRST
  {"$unwind": "..."},   // 2. Unwind if needed
  {"$project": {...}},  // 3. Select fields
  {"$group": {...}},    // 4. Aggregate
  {"$sort": {...}},     // 5. Sort results
  {"$skip": 5},         // 6. Skip (for pagination)
  {"$limit": 10},       // 7. Limit output
  {"$out": "results"}   // 8. Write (must be last)
]
```

---

# Example

```python

# Multi-stage pipeline
pipeline = [
    # Stage 1: Filter (like WHERE in SQL)
    {
        "$match": {
            "creditLimit": {"$gt": 50000}
        }
    },
    
    # Stage 2: Transform (like SELECT in SQL)
    {
        "$project": {
            "name": 1,
            "country": "$address.country",
            "creditLimit": 1,
            "_id": 0
        }
    },
    
    # Stage 3: Sort (like ORDER BY in SQL)
    {
        "$sort": {"creditLimit": -1}
    }
]
```

---

# Stages

- $match - https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/

```javascript

{ $match: { <query predicate> } }

```

- Example

```python
# Only customers from USA
usa_match = {"$match": {"country": "USA"}}

# Only high-value customers  
high_value_match = {"$match": {"creditLimit": {"$gt": 100000}}}
```

---

# Stages

- $project - https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/

```javascript

{ $project: { <specification(s)> } }

```

- Example

```python
basic_projection = {"$project": {"name": "$customerName", "creditLimit": 1, "_id": 0}}
```

---

# Stages

- $group

```javascript
{
 $group:
   {
     _id: <expression>, // Group key
     <field1>: { <accumulator1> : <expression1> },
     ...
   }
 }
```

---

# $group

- Count customer by country

```python
# Simple aggregation: count customers by country
pipeline = [
    {
        "$group": {
            "_id": "$address.country",           # Group by country
            "customerCount": {"$sum": 1}         # Count documents in each group
        }
    }
]

country_counts = customers.aggregate(pipeline)
print("Customers by country:")
for result in country_counts:
    print(f"- {result['_id']}: {result['customerCount']} customers")
```

---

# $group (cont.)

- Count customer by country and sort by descending


```python

# Same thing with more Pythonic approach
country_pipeline = [
    {"$group": {"_id": "$country", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}  # Sort by count descending
]

results = list(customers.aggregate(country_pipeline))
for result in results:
    country = result['_id'] or 'Unknown'
    count = result['count']
    print(f"{country}: {count} customers")
```

---

# Excercise

1. Find all customers in Europe (France, Germany, Spain)
2. Show only customer name and city
3. Sort by city name
4. Find products with low stock (< 1000)
5. Show product name, stock, and vendor
6. Sort by stock level (lowest first)
7. Count customers by country
8. Show countries with more than 10 customers
9. Sort by customer count

