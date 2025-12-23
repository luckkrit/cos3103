---
title: NoSQL - Tutorial
transition: fade
---

# NoSQL Tutorial

---

# Table of Contents

## Part 1: Database Fundamentals
- Database Connection
- PyMongo Setup
- Document Structure (Embedded vs Referencing)

## Part 2: Basic Operations
- Create Database and Collection
- Drop Database and Collection
- JSON Schema Validation
- Insert Documents

---

## Part 3: Querying
- Find Documents
- Comparison Operators
- Logical Operators
- Element Operators
- Arithmetic Operators
- String Operators
- Date Operators

---

## Part 4: Advanced Features
- Projection
- Sorting and Limiting
- Count and Distinct
- Migration from MySQL

## Part 5: Exercises
- Customer Queries
- Order and Product Queries
- Advanced Query Exercises

---
layout: cover
---

## Part 1: Database Fundamentals

---

# Database Connection

- **URI (Uniform Resource Identifier):** A database URI is a standardized string that contains all the information needed to connect to a database. It typically follows this format:

    ```
    protocol://username:password@host:port/database_name?options
    ```

    - MongoDB: `mongodb://user:password@localhost:27017/mydb`

    - The URI includes:

        - **Protocol/scheme**: Identifies the database type
        - **Credentials**: Username and password for authentication
        - **Host and port**: Where the database server is located
        - **Database name**: Which specific database to connect to
        - **Options**: Additional connection parameters (timeouts, SSL settings, etc.)

<StickyNote color="amber-light" textAlign="left" width="180px" title="Development" v-drag="[700,200,180,180]">


- No need to specify username and password
</StickyNote>

---


# Database Connection (cont.)

- **Driver :** A database driver is a software component that enables applications to communicate with a specific type of database. ==It acts as a translator between your application code and the database server.==


**Key functions:**

- Translates application requests into database-specific protocols
- Handles network communication with the database server
- Manages connection pooling and transaction handling
- Converts data types between the application and database formats


## Python

- PyMongo

---


# PyMongo

## PEP 249 - Python Database API Specification 2.0 ⚠️ (Partial)

- PyMongo does NOT fully follow PEP 249 because:

    1. MongoDB is NoSQL, not SQL
    2. Uses its own API design (find, insert_one, etc.)
    3. But it does follow: ==connection, cursor concepts==


---


# Setup MongoDB & Migration tools

- Setup MongoDB https://www.mongodb.com/try/download/community

- Download MySQL Connector/J 9.4.0 https://dev.mysql.com/downloads/connector/j/

- MongoDB Relational Migrator https://www.mongodb.com/try/download/relational-migrator

- Migrate classicmodels in MySQL to MongoDB https://www.youtube.com/watch?v=Z6D5Ge4M2KU

---

# Install PyMongo

```bash
pip install pymongo
```

---


# Document Structure

## Embeded

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


---

# Document Structure (cont.)

## Referencing

```python

customer_doc = {
  "_id": {
    "$oid": "68c902a2b612ea7e3090195a"
  },
  "customerNumber": 103,
  "customerName": "Atelier graphique",
  "contactLastName": "Schmitt",
  "contactFirstName": "Carine ",
  "phone": "40.32.2555",
  "addressLine1": "54, rue Royale",
  "addressLine2": null,
  "city": "Nantes",
  "state": null,
  "postalCode": "44000",
  "country": "France",
  "salesRepEmployeeNumber": 1370,
  "creditLimit": {
    "$numberDecimal": "21000.00"
  }
}

```
---

# Create connection

```python

from pymongo import MongoClient
uri = "mongodb://localhost:27017/"
def execute(callable):
    try:
        client = MongoClient(uri)
        callable(client)

        client.close()
    except Exception as e:
        raise Exception("Unable to find the document due to the following error: ", e)
```

---
layout: cover
---

## Part 2: Basic Operations

---

# Create Database and Collection
- ==The datbase does not exist until you insert the first documentation==

```python

def create_db(client):
    db = client.my_db # create database my_db
    users = db.users # or db['users'] ;create collection users
    users.insert_one({"username":"Alice", "email":"alice@gmail.com"}) # commented this line will not create database

execute(create_db)
```

---


# Drop Database and Collection
- Drop Database means removing all Collections in the Database
- Drop Collection means removing a specific Collection in the Database
    - ==If there is only 1 collection and it is dropped, the whole database is dropped too==



```python

from time import sleep
def test_create_drop_database(client, db_name, collection_name):
    db = client[db_name]
    collections = db[collection_name]
    collections.insert_one({})

    print(f"Wait for 10 seconds before drop Collection: {collection_name}")
    sleep(10)

    collections.drop()

    print(f"Wait for 10 seconds before drop Database: {db_name}")
    sleep(10)

    client.drop_database(db_name)

execute(lambda client:test_create_drop_database(client=client, db_name="test_db",collection_name="books"))
```

---


# List collections

- `list_collections()` - list collections: https://pymongo.readthedocs.io/en/4.15.1/api/pymongo/database.html#pymongo.database.Database.list_collections
- `list_collection_names()` - list collection names: https://pymongo.readthedocs.io/en/4.15.1/api/pymongo/database.html#pymongo.database.Database.list_collection_names


```python

def list_collections(client):
    db = client.my_db
    collection_list = db.list_collections()
    print("\nGet Collections:")
    for c in collection_list:
        print(c)

    print("\nGet Collection names:")
    collection_names = db.list_collection_names()
    for c in collection_names:
        print(c)

execute(list_collections)
```

---


# JSON Schema Validation

1. Schema validation create rules such as data types and values for fields 
2. MongoDB uses a flexible schema model by default. 


- `required` - must exist.

- `bsonType` - type checking.

```python
"$jsonSchema": {
      "bsonType": "object",
      "required": ["name", "age"],
      "properties": {
        "name": {
          "bsonType": "string",
          "description": "must be a string"
        },
        "age": {
          "bsonType": "int",
          "minimum": 0,
          "description": "must be a non-negative integer"
        }
      }
    }
```

---

# JSON Schema Validation (cont.)

```python


def create_users_collection(client):
    db = client.my_db
    db.create_collection("users", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "email"],
            "properties": {
                "username": {"bsonType": "string"},
                "email": {"bsonType": "string"},
                "dob": {"bsonType": "date"},
                "height": {"bsonType": "double"},
                "age": {"bsonType": "int"}
            }
        }
    })

execute(create_users_collection)
```

- Try insert invalid user

```python

def try_insert_users(client):
    db = client.my_db
    db.users.insert_one({"username":"Mike"})
execute(try_insert_users)
```

---


# Insert document 

- Insert single document https://pymongo.readthedocs.io/en/4.15.1/api/pymongo/collection.html#pymongo.collection.Collection.insert_one

```python
insert_one(document, bypass_document_validation=None, session=None, comment=None)
```

- Insert multiple documents https://pymongo.readthedocs.io/en/4.15.1/api/pymongo/collection.html#pymongo.collection.Collection.insert_many

```python
insert_many(documents, ordered=True, bypass_document_validation=None, session=None, comment=None)
```

---

- Insert one

```python

from datetime import datetime
def insert_user(client, user):
    db = client.my_db
    users = db.users
    users.insert_one(user)

execute(lambda client: insert_user(client=client,
                                   user={"username":"Alice", 
                                         "email":"alice@gmail.com",
                                         "age":45,
                                         "dob":datetime(1979, 1, 11),
                                         "height": 155.45}))
```

---

- Insert many

```python

from datetime import datetime
def insert_multiple_users(client, user_list):
    db = client.my_db
    users = db.users
    users.insert_many(user_list)

execute(lambda client: insert_multiple_users(client=client,
                                   user_list=[{
                                       "username":"Jane", 
                                       "email":"jane@gmail.com",
                                       "age": 33,
                                       "dob": datetime(1992, 2, 22),
                                       "height": 160.35
                                       },{
                                           "username":"Bob",
                                           "email":"bob@gmail.com",
                                       "age": 31,
                                       "dob": datetime(1994, 8, 13),
                                       "height": 165.35
                                       }]))
```

---
layout: cover
---

## Part 3: Querying

---


# Find documents

- find https://pymongo.readthedocs.io/en/4.15.1/api/pymongo/collection.html#pymongo.collection.Collection.find

```python
find(filter=None, projection=None, skip=0, limit=0, no_cursor_timeout=False, cursor_type=CursorType.NON_TAILABLE,
 sort=None, allow_partial_results=False, oplog_replay=False, batch_size=0, collation=None, hint=None, max_scan=None, 
 max_time_ms=None, max=None, min=None, return_key=False, show_record_id=False, snapshot=False, comment=None, session=None, 
 allow_disk_use=None)
```

- find_one https://pymongo.readthedocs.io/en/4.15.1/api/pymongo/collection.html#pymongo.collection.Collection.find_one

```python
find_one(filter=None, *args, **kwargs)
```

---

- Find all

```python

def find_all_user(client, filter):
    db = client.my_db
    users = db.users
    for u in users.find(filter):
        print(u)


execute(lambda client: find_all_user(client=client, filter={}))
```

- Find one

```python

def find_one_user(client, filter):
    db = client.my_db
    users = db.users
    print(users.find_one(filter))

execute(lambda client: find_one_user(client=client, filter={}))
```

---

# Find excact match

- find with query that match specific field and value

```python
def find_user_exact_match(client, filter):
    db = client.my_db
    users = db.users
    for user in users.find(filter):
        print(user)

print("1. find user name is Alice")
execute(lambda client: find_user_exact_match(client=client, filter={'username':'Alice'}))
print("\n2. find user whose age is 33")
execute(lambda client: find_user_exact_match(client=client, filter={'age':33}))

```

---

# Comparison Operators


|Operator|Description|
|:--|:--|
|`$eq`|Matches values that are equal to a specified value.|
|`$gt`|Matches values that are greater than a specified value.|
|`$gte`|Matches values that are greater than or equal to a specified value.|
|`$in`|Matches any of the values specified in an array.|
|`$lt`|Matches values that are less than a specified value.|
|`$lte`|Matches values that are less than or equal to a specified value.|
|`$ne`|Matches all values that are not equal to a specified value.|
|`$nin`|Matches if the value is not equal to any of a given list of values.|

---

# Comparison Operators (cont.)

- https://www.mongodb.com/docs/manual/reference/mql/query-predicates/comparison/

```python

from datetime import datetime
def find_user_by_age(client,filter):
    db = client.my_db
    users = db.users
    user_ages = users.find(filter)
    for user in user_ages:
        print(user)

print("1. Find users by age more than 30")
execute(lambda client: find_user_by_age(client=client, filter={'age':{'$gt': 30}}))

print("\n2. Find users by dob in ranges ['1979-01-11','1994-08-13']")
execute(lambda client: find_user_by_age(client=client, filter={'dob':{'$in': [datetime(1979,1,11),datetime(1994,8,13)]}}))

print("\n3. Find users by dob not in ranges ['1979-01-11','1994-08-13']")
execute(lambda client: find_user_by_age(client=client, filter={'dob':{'$nin': [datetime(1979,1,11),datetime(1994,8,13)]}}))

```

---

# Logical Operators

- https://www.mongodb.com/docs/manual/reference/mql/query-predicates/logical/

|Name|Description|
|:--|:--|
|`$and`|Joins query clauses with a logical AND and returns documents that match the conditions of all clauses.|
|`$nor`|Joins query clauses with a logical NOR and returns all documents that fail to match all clauses.|
|`$not`|Inverts the effect of a query predicate and returns documents that do not match the query predicate.|
|`$or`|Joins query clauses with a logical OR and returns all documents that match at least one clause.|

---


```python
def find_users_by_height(client, filter):
    db = client.my_db
    users = db.users
    for user in users.find(filter):
        print(user)

print("1. implicit AND operator")
execute(lambda client:find_users_by_height(client=client, filter={'height':{'$lt':165,'$gt':160}}))
print("\n2. explicit AND operator")
execute(lambda client:find_users_by_height(client=client, filter={'$and':[{'height':{'$lt':165}},{'height':{'$gt':160}}]}))
print("\n3. Implicit AND with multiple fields")
execute(lambda client: find_users_by_height(
    client=client,
    filter={
        'height': {'$gte': 160},
        'username': {'$in': ['Alice', 'Bob', 'Jane']}
    }
))
print("\n4. Explicit AND with OR")
execute(lambda client: find_users_by_height(
    client=client,
    filter={'$and': [
        {'$or': [
            {'height': {'$lt': 165}},{'height': {'$gt': 160}}
        ]},
        {'age': {'$gt':30,'$lt':35}} 
    ]}
))

```

---


# Element Operators

- `$exists` : Element operators query data based on the presence or type of a field.

- Example

```python

def find_user_with_age_exists(client, filter):
    db = client.my_db
    users = db.users
    for user in users.find(filter):
        print(user)

execute(lambda client: find_user_with_age_exists(client=client,filter={'age':{'$exists': True}}))
```

---

# Misc Operators


- `$expr` can contain expressions that compare fields from the same document.



- Find users older than 18 

```python
db.users.find({ "age": { "$gt": 18 } })
```


- Find users older than min age

    - $expr means expression
    
    - "${field}" means “use the value from this field”

```python
db.users.find({
  "$expr": { "$gt": ["$age", "$minAge"] }
})
```

---

- Find users that age less than height

```python

def find_user_where_age_less_than_height(client,filter):
    db = client.my_db
    users = db.users
    for user in users.find(filter):
        print(user)

execute(lambda client: find_user_where_age_less_than_height(client=client, filter={'$expr':{'$lt':['$age','$height']}}))
```

---

- Find users whose score is greater than passing score and over 30 years

```python
db.users.find({
  "$expr": {
    "$and": [
      { "$gt": ["$score", "$passingScore"] },
      { "$lt": ["$age", 30] }
    ]
  }
})
```
---

# Arithmetic Operators

- `$add` - Addition: `{$add: ["$field1", "$field2"]}`
- `$subtract` - Subtraction: `{$subtract: ["$field1", "$field2"]}`
- `$multiply` - Multiplication: `{$multiply: ["$field1", 2]}`
- `$divide` - Division: `{$divide: ["$field1", "$field2"]}`
- `$mod` - Modulo: `{$mod: ["$field1", 10]}`
- `$abs` - Absolute value: `{$abs: "$field1"}`
- `$ceil` - Round up: `{$ceil: "$price"}`
- `$floor` - Round down: `{$floor: "$price"}`
- `$round` - Round to nearest: `{$round: ["$price", 2]}`

---

# Example 1: $add - Find students with total score > 250

```python
def add_students(client, students_data):
    db = client.my_db
    students = db.students
    students.insert_many(students_data)

students_data = [
    {"name": "Alice Johnson", "math": 85, "science": 92, "english": 78, "credits": 18},
    {"name": "Bob Smith", "math": 72, "science": 68, "english": 85, "credits": 15},
    {"name": "Carol Davis", "math": 95, "science": 88, "english": 92, "credits": 21},
    {"name": "David Wilson", "math": 67, "science": 74, "english": 81, "credits": 12},
    {"name": "Emma Brown", "math": 89, "science": 91, "english": 87, "credits": 20},
    {"name": "Frank Miller", "math": 76, "science": 82, "english": 79, "credits": 16},
    {"name": "Grace Lee", "math": 93, "science": 96, "english": 94, "credits": 22},
    {"name": "Henry Taylor", "math": 81, "science": 75, "english": 83, "credits": 18}
]

execute(lambda client: add_students(client=client, students_data=students_data))
```
---

```python

def find_students(client, filter):
    db = client.my_db
    students = db.students
    for student in students.find(filter):
        print(student)

execute(lambda client: find_students(client=client,filter={
    '$expr':{
        '$gt':[
            {
                '$add':['$math', '$science', '$english']
            },
            250]
        }
    }))
```

---

# Example 2: $subtract - Find products with profit > $100 

```python

def add_products(client, products_data):
    db = client.my_db
    products = db.products
    products.insert_many(products_data)

products_data = [
    {"name": "Laptop", "costPrice": 800, "sellingPrice": 1200, "quantity": 50},
    {"name": "Mouse", "costPrice": 15, "sellingPrice": 25, "quantity": 200},
    {"name": "Keyboard", "costPrice": 45, "sellingPrice": 75, "quantity": 120},
    {"name": "Monitor", "costPrice": 250, "sellingPrice": 400, "quantity": 80},
    {"name": "Headphones", "costPrice": 60, "sellingPrice": 99, "quantity": 150},
    {"name": "Webcam", "costPrice": 35, "sellingPrice": 65, "quantity": 90},
    {"name": "Speaker", "costPrice": 80, "sellingPrice": 130, "quantity": 60},
    {"name": "Tablet", "costPrice": 300, "sellingPrice": 450, "quantity": 40}
]

execute(lambda client: add_products(client=client, products_data=products_data))
```

---

```python


def find_products(client, filter):
    db = client.my_db
    products = db.products
    for product in products.find(filter):
        print(product)

execute(lambda client: find_products(client=client, filter={
    '$expr':{
        '$gt':[{
            '$subtract':[
                '$sellingPrice',
                '$costPrice'
            ]
        },100]
    }
}))
```

---

# Example 3: $multiply - Find sales with revenue > $1000

```python
from datetime import datetime
def add_product_sales(client, sales_data):
    db = client.my_db
    product_sales = db.product_sales
    product_sales.insert_many(sales_data)

sales_data = [
    {"product": "Laptop", "quantity": 5, "unitPrice": 1200, "date": datetime(2024, 1, 15)},
    {"product": "Mouse", "quantity": 20, "unitPrice": 25, "date": datetime(2024, 1, 16)},
    {"product": "Keyboard", "quantity": 8, "unitPrice": 75, "date": datetime(2024, 1, 17)},
    {"product": "Monitor", "quantity": 3, "unitPrice": 400, "date": datetime(2024, 1, 18)},
    {"product": "Headphones", "quantity": 12, "unitPrice": 99, "date": datetime(2024, 1, 19)},
    {"product": "Laptop", "quantity": 2, "unitPrice": 1200, "date": datetime(2024, 1, 20)},
    {"product": "Tablet", "quantity": 6, "unitPrice": 450, "date": datetime(2024, 1, 21)},
    {"product": "Speaker", "quantity": 4, "unitPrice": 130, "date": datetime(2024, 1, 22)}
]

execute(lambda client: add_product_sales(client=client, sales_data=sales_data))
```

---

```python

def find_product_sales(client, filter):
    db = client.my_db
    product_sales = db.product_sales
    for product in product_sales.find(filter):
        print(product)

execute(lambda client: find_product_sales(client=client, filter={
    '$expr':{
        '$gt':[
            {
                '$multiply':[
                    '$quantity',
                    '$unitPrice'
                ]
            },
            1000
        ]
    }
}))
```

---

# Example 4: $divide - Find students with average grade > 85

```python

execute(lambda client: find_students(client=client, filter={
    '$expr':{
        '$gt':[{
            '$divide':[
                {
                    '$add':['$math','$science','$english']
                },
                3
            ]
        },
        85
        ]
    }
}))
```


---

# String Operators

1. `$strLenCP` - String length calculations `{ "$strLenCP": "$name" }`

2. `$toLower` / `$toUpper` - Case conversion `{ "$toLower": "$name" }` / `{ "$toUpper": "$name" }`

3. `$substr` - Substring extraction `{ $substr: [ <string>, <start>, <length> ] }`

4. `$concat` - String concatenation `{ $concat: [ <expression1>, <expression2>, ... ] }`

5. `$indexOfCP` - Find character positions `{ $indexOfCP: [ <string expression>, <substring expression>, <start>, <end> ] }`

6. `$toString` - Convert numbers to strings `{$toString: <expression>}`

---

# Add aditional students and products data

- additonal students

```python

additional_students = [
    {"name": "Anna-Maria Smith", "math": 88, "science": 85, "english": 92, "email": "anna.smith@university.edu"},
    {"name": "JOHN DOE", "math": 75, "science": 80, "english": 78, "email": "john.doe@COLLEGE.EDU"},
    {"name": "mary johnson", "math": 90, "science": 87, "english": 89, "email": "mary.j@school.org"},
    {"name": "Robert-Jr Wilson", "math": 82, "science": 76, "english": 88, "email": "robert.wilson@uni.ac.uk"}
]

execute(lambda client: add_students(client=client, students_data=additional_students))
```

- additional products

```python

additional_products = [
    {"name": "Gaming Laptop Pro", "category": "Electronics", "brand": "TechCorp", "model": "GLP-2024"},
    {"name": "wireless mouse", "category": "accessories", "brand": "MouseMaker", "model": "WM-150"},
    {"name": "MECHANICAL KEYBOARD", "category": "ACCESSORIES", "brand": "KeyBoard Inc", "model": "MK-RGB"},
    {"name": "Ultra-HD Monitor", "category": "Electronics", "brand": "ScreenTech", "model": "UHD-27"}
]

execute(lambda client: add_products(client=client, products_data=additional_products))
```

---

# Example 1: $concat - Find students whose name length > 12 characters

```python
execute(lambda client: find_students(client=client, filter={
    '$expr':{
        '$gt':[
            {
                '$strLenCP': '$name'
            }
            ,
            12
        ]
    }
}))
```

---

# Example 2: $toLower - Find students with lowercase names

```python

execute(lambda client: find_students(client=client, filter={
    '$expr':{
        '$eq':[
            '$name',
            {
                '$toLower': '$name'
            }
        ]
    }
}))
```
---


# Example 3: $toUpper - Find products with uppercase names

```python

execute(lambda client: find_products(client=client, filter={
    '$expr':{
        '$eq':[
            '$name',
            {
                '$toUpper':'$name'
            }
        ]
    }
}))
```

---

# Example 4: $substr - Find students whose first 4 characters are "Anna"

```python

execute(lambda client: find_students(client=client, filter={
    '$expr':{
        '$eq':[
            {
                '$substr': ['$name',0,4]
            },
            'Anna'
        ]
    }
}))
```

---

# Example 5: $concat - Create full display name and compare length

```python

execute(lambda client: find_students(client=client, filter={
    '$expr':{
        '$gt':[
            {
                '$strLenCP':{
                    '$concat':[
                        'Name :',
                        '$name'
                        ]
                }
            }
            ,20
        ]
    }
}))
```

---

# Example 6: Complex string operation - Email domain extraction

```python

execute(lambda client: find_students(client=client, filter={
    '$and': [
        {'email': {'$exists': True}},
        {'email': {'$ne': ''}},  # Also ensure it's not empty
        {'$expr': {'$eq': [
            {'$substr': [
                '$email',
                {'$subtract': [{'$strLenCP': '$email'}, 4]},
                4
            ]}, '.edu'
        ]}}
    ]
}))
```

---

# Date Operators

1. $year - extract year `{ $year: <dateExpression> }`
2. $month - extract month `{ $month: <dateExpression> }`
3. $dayOfMonth - extract day of month `{ $dayOfMonth: <dateExpression> }`

---

# Example 1: $year - Find users born in specific year

```python
execute(lambda client: find_all_user(
    client=client, 
    filter={'$expr': {'$eq': [{'$year': '$dob'}, 1979]}}
))
```
# Example 2: $month - Find users born in specific month

```python
execute(lambda client: find_all_user(
    client=client, 
    filter={'$expr': {'$eq': [{'$month': '$dob'}, 8]}}
))
```


# Example 3: $dayOfMonth - Find users born in specific day of month

```python
execute(lambda client: find_all_user(
    client=client, 
    filter={'$expr': {'$eq': [{'$dayOfMonth': '$dob'}, 13]}}
))
```

---
layout: cover
---

## Part 4: Advanced Features

---

# Find document and projection
- projection: specify which fields to include or exclude
    - list shorthand: use list for simple inclusion
      `projection = ["email"]` - include `email` (and `_id` automatically)
    - inclusive (whitelist): use dict with `True`/`1` values
      `projection = {"email": True, "_id": False}` - include only email
    - exclusive (blacklist): use dict with `False`/`0` values  
      `projection = {"_id": False, "email": False}` - exclude these fields

---

```python

def find_users(client, filter, projection):
    db = client.my_db
    users = db.users
    for u in users.find(filter, projection): 
        print(u)

print("1 - include every fields")
execute(lambda client: find_users(client=client, filter={}, projection=[])) 
print("\n2 - include email and always include _id")
execute(lambda client: find_users(client=client, filter={}, projection=["email"])) 
print("\n3 - include only email and username not _id")
execute(lambda client: find_users(client=client, filter={}, projection={"_id":False,"email":True, "username": True})) 
print("\n4 - exclusive all")
execute(lambda client: find_users(client=client, filter={}, projection={"_id":False,"email":False, "username": False})) 
# print("\n5 - error cannot mix inclusive fields and exclusive fields")
# error cannot mix inclusive and exclusive, no need to specify username because it already include by default
# execute(lambda client: find_users(client=client, filter={}, projection={"_id":False,"email":False, "username": True})) 
```

- Show all fields except _id ?

---


# Find documents with limited size
- use `limit(10)` to get only 10 documents
- use `skip(5)` to skip the first 5 documents

```python

def find_users_by_size(client, filter, projection, limit=0, skip=0):
    db = client.my_db
    users = db.users
    for u in users.find(filter, projection, limit=limit, skip=skip): 
        print(u)

print("1 - print only 2 results")
execute(lambda client: find_users_by_size(client=client, filter={}, projection=[], limit=2)) # include every fields
print("\n2 - print only 2 results and skip 1 row")
execute(lambda client: find_users_by_size(client=client, filter={}, projection=[], limit=2, skip=1)) # include every fields

```

---


# Sorting Documents

- Ascending: `1` / `pymongo.ASCENDING`
- Descending: `-1`/ `pymongo.DESCENDING`

```python

import pymongo
def find_user_sort(client, filter, sort_by, direction=pymongo.ASCENDING):
    db = client.my_db
    users = db.users
    for user in users.find(filter).sort(sort_by,direction):
        print(user)

print("1. Sort by height ascending")
execute(lambda client: find_user_sort(client=client, filter={},sort_by="height"))
print("\n2. Sort by height descending")
execute(lambda client: find_user_sort(client=client, filter={},sort_by="height", direction=-1))

```

---


# Count Documents Returned from a Query

- count documents - https://pymongo.readthedocs.io/en/4.15.1/api/pymongo/collection.html#pymongo.collection.Collection.count_documents 

```python
count_documents(filter, session=None, comment=None, **kwargs)
```

- Example

```python

def count_users(client, filter):
    db = client.my_db
    users = db.users
    print(users.count_documents(filter))

execute(lambda client: count_users(client=client,filter={"username":"Alice"}))
```

---

# Retrieve Distinct Values

```python
distinct(key, filter=None, session=None, comment=None, hint=None, **kwargs)
```

- Example

```python
def find_distinct_username(client, distinct_field):
    db = client.my_db
    users = db.users
    distinct_users = users.distinct(distinct_field)
    for user in distinct_users:
        print(user)

execute(lambda client: find_distinct_username(client=client,distinct_field="username"))

```

--- 

# Migration

- Migrate from MySQL to MongoDB
- Convert table `customers` and `product` to embeded structure

---
layout: cover
---

## Part 5: Exercises

---

# Exercise


1. Find customers where salesRepEmployeeNumber is '1166' or 1166. Which one gets results?
2. Find customer by customerNumber is 103
3. Find customers where state is NULL
4. Find customers where city is San Francisco
5. Find customers where postalCode is 97562 
6. Find customers where creditLimit is between 50,000 and 100,000
7. Find customers who are in USA and France whose creditLimit is between 10,000 and 80,000 
8. Find customers whose creditLimit is less than 100,000
9. Find customers who have placed orders (customers with existing orders)
10. Find customers in California (CA) with creditLimit greater than 50,000, sorted by creditLimit descending

---

# Exercise (cont.)

11. Find orders placed in 2003
12. Find orders with status 'Shipped' or 'Resolved'
13. Find orders that have comments/notes
14. Find orders where requiredDate is in December 2004
15. Find products with quantityInStock less than 1000
16. Find products where productName contains "Ford"
17. Find products with buyPrice between $50 and $100
18. Find products in productLine 'Classic Cars' or 'Vintage Cars'
19. Find employees with jobTitle 'Sales Rep'
20. Find employees in office code 1, 2, or 3

---

# Exercise (cont.)

21. Find payments made in 2004 with amount greater than $50,000
22. Find employees in office codes 1, 4, or 6
23. Find offices located in countries other than USA
24. Find products where MSRP is more than twice the buyPrice
25. Find customers with creditLimit exactly equal to 50000
26. Find orders where shippedDate is later than requiredDate
27. Find employees with jobTitle exactly 'Sales Manager'
28. Find products with productScale '1:18' or '1:24'
29. Find customers in states 'CA', 'NY', or 'TX'
30. Find order details where quantityOrdered is greater than 40 and priceEach is less than $100

---

# Exercise (cont.)

- From my_db database

31. Find employees where total salary (baseSalary + bonus) > $5000"
32. Find products where selling price is more than double the cost price"
33. Find students with more than 18 credits AND average grade > 80"
34. Find sales where revenue is less than $500"
35. Find hourly employees (hourlyRate > 0) with total pay > $3000"