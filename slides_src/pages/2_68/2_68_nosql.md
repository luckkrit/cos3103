---
layout: section
transition: fade
---

# NoSQL Tutorial

---

# Migration

![migration](/images/2_68_nosql/chrome_4tBnFjJDLq.gif)

---

# Setup Nodejs

1. Download: https://nodejs.org/dist/v25.7.0/node-v25.7.0-x64.msi

---

# Create Project

```bash
mkdir mongo_tutorial
cd mongo_tutorial
npm init -y 
npm install mongodb@7.1
```

---

# Create Connection

- index.js

```js
const { MongoClient } = require('mongodb');

async function runGetStarted() {
    // Replace the uri string with your connection string
    const uri = 'mongodb://localhost:27017/';
    const client = new MongoClient(uri);
    try {
    } finally {
        await client.close();
    }
}
runGetStarted().catch(console.dir);

```

---
layout: two-cols-title
---

::title::
# Create Collection and Document

::left::

- tutorial.js

```js
module.exports = {
    // Create Collection and Document
    ex1: async function (client) {
        const db = client.db('my_mongo')
        const users = db.collection('users')
        const result = await users.insertOne(
            { "username": "Alice", "email": 
            "alice@gmail.com" })
        console.log(`A document was inserted with the _id: 
        ${result.insertedId}`);
    }
} 
```
::right::

- index.js

```js
const { MongoClient } = require('mongodb');
const tutorial = require('./tutorial.js')

async function runGetStarted() {
    // Replace the uri string with your connection string
    const uri = 'mongodb://localhost:27017/';
    const client = new MongoClient(uri);
    try {
        await tutorial.ex1();
    } finally {
        await client.close();
    }
}
runGetStarted().catch(console.dir);

```
::default::


---

# List Collections

```js

    // List collections
    ex3: async function (client) {
        const db = client.db('pg_classic')
        const collections = db.listCollections()
        console.log('\nGet Collections:')
        for await (const c of collections) {
            console.log(c)
        }
        console.log('\nGet Collection names:')
        const collectionNames = db.listCollections({}, { nameOnly: true })
        for await (const n of collectionNames) {
            console.log(n)
        }
    }
```

---

# Insert many documents

```js

    // Insert many documents
    ex4: async function (client) {
        const db = client.db('my_mongo')
        const users = db.collection('users')
        const insertManyresult = await users.insertMany([
         { "username": "Alice", "email": "alice@gmail.com" },
         { username: 'Jack', email: 'jack@gmail.com' }])
        let ids = insertManyresult.insertedIds;
        console.log(`${insertManyresult.insertedCount} documents were inserted.`);
        for (let id of Object.values(ids)) {
            console.log(`Inserted a document with id ${id}`);
        }
    }
```

---

# Find documents

```js
    // Find all and find one
    ex5: async function (client) {
        const db = client.db('my_mongo')
        const users = db.collection('users')
        console.log('find all')
        console.log('--------------')
        const findResult = users.find()
        for await (const doc of findResult) {
            console.log(doc);
        }
        console.log('find one')
        console.log('--------------')
        const findOneResult = await users.findOne();
        console.log(findOneResult)
    },
```

---

# Find exact match

```js
    // Find excact match
    ex6: async function (client) {
        const db = client.db('my_mongo')
        const users = db.collection('users')
        const findResult = await users.find({ username: 'Jack' })
        for await (const doc of findResult) {
            console.log(doc);
        }
    }
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

# Greater than

```js
    // Comparison Operators
    ex7: async function (client) {
        const { Decimal128 } = require('mongodb');
        const db = client.db('pg_classic')
        const orderdetails = db.collection('orderdetails')
        const findResult = await orderdetails.find({ priceeach: { $gt: 83.44 } }) // driver convert to Decimal128
        for await (const doc of findResult) {
            console.log(doc.priceeach);
        }
        console.log('-------------')
        const findResult2 = await orderdetails.find({ priceeach: { $in: [Decimal128.fromString("83.44")] } })
        for await (const doc of findResult2) {
            console.log(doc.priceeach);
        }
        console.log('-------------')
        const findResult3 = await orderdetails.find({ priceeach: { $eq: Decimal128.fromString("83.44") } })
        for await (const doc of findResult3) {
            console.log(doc.priceeach);
        }
    }
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

# And

```js

    // Logical Operators
    ex8: async function (client) {
        const { Decimal128 } = require('mongodb');
        const db = client.db('pg_classic')
        const orderdetails = db.collection('orderdetails')
        const findResult = await orderdetails.find({ priceeach: { $gt: 83.44, $lt: 84 } }) // driver convert to Decimal128
        for await (const doc of findResult) {
            console.log(doc.priceeach);
        }
        console.log('-------------')
        const findResult2 = await orderdetails.find({ $and: [{ priceeach: { $gt: 83.44 } }, { priceeach: { $lt: 84 } }] })
        for await (const doc of findResult2) {
            console.log(doc.priceeach);
        }
        console.log('-------------')
        const findResult3 = await orderdetails.find({ priceeach: { $lt: 30.00 }, quantityordered: { $lt: 30.00 } })
        for await (const doc of findResult3) {
            console.log(doc.ordernumber, doc.priceeach, doc.quantityordered);
        }
    }
```

---

# MongoDb Shell

- not use Decimal128 but `{priceeach: new NumberDecimal('29.54')}`


![2_68_nosql_2026-02-28-16-35-05](/images/2_68_nosql/2_68_nosql_2026-02-28-16-35-05.png)


---

# Misc Operators


- `$expr` can contain expressions that compare fields from the same document.



- Find products where buyprice less than msrp

```js
    // Expression Operator
    ex9: async function (client) {
        const db = client.db('pg_classic')
        const products = db.collection('products')
        const findResult = await products.find({ $expr: { $lt: ["$buyprice", "$msrp"] } })
        for await (const doc of findResult) {
            console.log(doc.productcode, doc.buyprice, doc.msrp);
        }
    }
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

# Multiply

- Find order where sale amount > 10000

```js

    // Arithmetic Operator
    ex10: async function (client) {
        const db = client.db('pg_classic')
        const products = db.collection('orderdetails')
        const findResult = await products.find({
            $expr: {
                $gt: [{
                    $multiply: ["$quantityordered",
                        "$priceeach"]
                }, 10000]
            }
        })
        for await (const doc of findResult) {
            console.log(doc.ordernumber, Number(doc.priceeach), doc.quantityordered, 
            Number(doc.priceeach) * doc.quantityordered);
        }
    }
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

# String Length

- Find customers whose name is longer than 30 characters

```js
    // String Operator
    ex11: async function (client) {
        const db = client.db('pg_classic')
        const customers = db.collection('customers')
        const findResult = await customers.find({
            $expr: {
                $gt: [{ "$strLenCP": "$customername" }, 30]
            }
        })
        for await (const doc of findResult) {
            console.log(doc.customername, doc.customername.length);
        }
    }
```

---

# Date Operators

1. $year - extract year `{ $year: <dateExpression> }`
2. $month - extract month `{ $month: <dateExpression> }`
3. $dayOfMonth - extract day of month `{ $dayOfMonth: <dateExpression> }`

---

# Day of month

- Find payment date of 30

```js
    // Date Operator
    ex12: async function (client) {
        const db = client.db('pg_classic')
        const payments = db.collection('payments')
        const findResult = await payments.find({
            $expr: {
                $eq: [{ "$dayOfMonth": "$paymentdate" }, 30]
            }
        })
        for await (const doc of findResult) {
            console.log(doc.customernumber, doc.paymentdate.getDate());
        }
    }
```

---

# Find document and projection
- projection: specify which fields to include or exclude
    - list shorthand: use list for simple inclusion
      `projection = ["email"]` - include `email` (and `_id` automatically)
    - inclusive (whitelist): use dict with `true`/`1` values
      `projection = {"email": true, "_id": false}` - include only email
    - exclusive (blacklist): use dict with `false`/`0` values  
      `projection = {"_id": false, "email": false}` - exclude these fields


---

# Hide _id field

```js
    // Projection
    ex13: async function (client) {
        const db = client.db('pg_classic')
        const customers = db.collection('customers')
        const findResult = await customers.find({}).project({ "_id": false })
        for await (const doc of findResult) {
            console.log(doc._id, doc.customernumber, doc.customername);
        }
    }
```

---

# Find documents with limited size
- use `limit(10)` to get only 10 documents
- use `skip(5)` to skip the first 5 documents

```js
    // Limit and Skip
    ex14: async function (client) {
        const db = client.db('pg_classic')
        const customers = db.collection('customers')
        const findResult = await customers.find({})
        .project({ "_id": false }).limit(5).skip(5)
        for await (const doc of findResult) {
            console.log(doc.customernumber, doc.customername);
        }
    }
```

---

# Sorting Documents

- Ascending: `1` / `asc` / `ascending`
- Descending: `-1`/ `desc` / `descending`

https://mongodb.github.io/node-mongodb-native/7.1/types/SortDirection.html

![2_68_nosql_2026-02-28-20-44-08](/images/2_68_nosql/2_68_nosql_2026-02-28-20-44-08.png)

---

# Sort by customer number descending

```js
    // Sort
    ex15: async function (client) {
        const db = client.db('pg_classic')
        const customers = db.collection('customers')
        const findResult = await customers.find({}).project({ "_id": false }).limit(5).sort({ 'customernumber': 'desc' })
        for await (const doc of findResult) {
            console.log(doc.customernumber, doc.customername);
        }
    }
```
---

# Count Documents Returned from a Query

```js
    // Count
    ex16: async function (client) {
        const db = client.db('pg_classic')
        const customers = db.collection('customers')
        const countUSACustomers = await customers.countDocuments({ "country": "USA" })
        console.log(`Total customer in USA = ${countUSACustomers}`)
    }
```

---

# Retreive Distinct Values

```js

    // Distinct
    ex17: async function (client) {
        const db = client.db('pg_classic')
        const orders = db.collection('orders')
        const findResult = await orders.distinct('customernumber')
        for (const customernumber of findResult) {
            console.log(customernumber);
        }
    }
```

---

# What is Aggregation?

- Aggregation is like a data processing pipeline - you put documents in one end, and they get transformed step by step until you get the results you want.

<div class="w-[700px] mx-auto">

![Aggregation Pipeline](https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F2809lspwb4ah36t87e2r.jpg)

</div>

```js

// Defines and executes the aggregation pipeline
const results = await collection.aggregate([
  { $match: { ... } },
  { $group: { ... } }
]);

```

---

# Using $match

- Find products where productline is Motorcycles and buyprice is less than 60

```js
    // Aggregate $match
    ex18: async function (client) {
        const db = client.db('pg_classic')
        const products = db.collection('products')
        const findResult = await products.aggregate([{ "$match": { "productline": "Motorcycles", "buyprice": { "$lt": new Decimal128('60') } } }])
        for await (const product of findResult) {
            console.log(product);
        }
    }
```

---

# Using $match, $project, $sort, $limit

- Find product name, buyprice, productline where productline is motorcycles and buyprice is less than 60

```js

    // Aggreate $match, $project, $sort, $limit
    ex19: async function (client) {
        const db = client.db('pg_classic')
        const products = db.collection('products')
        const findResult = await products.aggregate([
            { "$match": { "productline": "Motorcycles", "buyprice": { "$lt": new Decimal128('60') } } },
            { "$project": { productname: true, buyprice: true, productline: true, _id: false } },
            { "$sort": { "buyprice": -1 } }, // allow -1 (desc) and 1 (asc)
            { "$limit": 3 }
        ])
        for await (const product of findResult) {
            console.log(product);
        }
    }
```

---

# Using $lookup

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

# Using $lookup and $project

- Find productcode,quantityorder,productname,buyprice,line from orderdetails join with products on productcode

==$lookup returns an array (product_order), even if there's only one match.==

```js
    // Aggreate $lookup, $project
    ex20: async function (client) {
        const db = client.db('pg_classic')
        const orderdetails = db.collection('orderdetails')
        const findResult = await orderdetails.aggregate([{
                "$lookup": {
                    "from": "products",
                    "localField": "productcode",
                    "foreignField": "productcode",
                    "as": "product_order"
                }
            },
            { "$project": { productcode: true, quantityordered: true, "product_order.productname": true, 
            "product_order.buyprice": true, "product_order.productline": true, _id: false } },
        ])
        for await (const product of findResult) {
            console.log(product);
        }
    }
```
---

# Using $unwind

- using `$unwind` to destruct array of product_order from previous example

```js
    // Aggreate $lookup, $project, $unwind
    ex21: async function (client) {
        const db = client.db('pg_classic')
        const orderdetails = db.collection('orderdetails')
        const findResult = await orderdetails.aggregate([
            {
                "$lookup": {
                    "from": "products",
                    "localField": "productcode",
                    "foreignField": "productcode",
                    "as": "product_order"
                }
            },
            { "$unwind": "$product_order" }, // match field must begin with $
            { "$project": { productcode: true, quantityordered: true, "product_order.productname": true, 
            "product_order.buyprice": true, "product_order.productline": true, _id: false } },
        ])
        for await (const product of findResult) {
            console.log(product);
        }
    }
```

---

# Using $addFields

- using `$addFields` - Adds new fields to documents. 

```js
    // Aggreate $lookup, $project, $unwind
    ex22: async function (client) {
        const db = client.db('pg_classic')
        const orderdetails = db.collection('orderdetails')
        const findResult = await orderdetails.aggregate([{
                "$lookup": {
                    "from": "products",
                    "localField": "productcode",
                    "foreignField": "productcode",
                    "as": "product_order"
                }
            },
            { "$unwind": "$product_order" }, // match field must begin with $
            { "$addFields": { "productname": "$product_order.productname", "buyprice": "$product_order.buyprice", 
            "productline": "$product_order.productline" } }, // match field must begin with $
            { "$project": { productcode: true, quantityordered: true, "productname": true, "buyprice": true, 
            "productline": true, _id: false } },
        ])
        for await (const product of findResult) {
            console.log(product);
        }
    },
```

---

# Using $group and $sum

- `SELECT COUNT(*) AS count FROM orders`

- using aggregate `$group` and `$sum`

```js

    // Aggregate $group, $sum
    ex23: async function (client) {
        const db = client.db('pg_classic')
        const orders = db.collection('orders')
        const findResult = await orders.aggregate([{
            "$group": {
                "_id": null, // grouping all documents into a single group
                "count": { "$sum": 1 }
            }
        }])
        for await (const product of findResult) {
            console.log(product);
        }
    },
```

---

# Using $count

- `SELECT COUNT(*) AS count FROM orders`

- using aggreate `$count`

```js
    // Aggregate $count
    ex23: async function (client) {
        const db = client.db('pg_classic')
        const orders = db.collection('orders')
        const findResult = await orders.aggregate([{
            "$count": 'count'
        }])
        for await (const product of findResult) {
            console.log(product);
        }
    },
```

---
layout: two-cols-title
---

::title::
# Example 10:

- `select o.customerNumber, sum(d.quantityOrdered * d.priceEach) as total from orders o left join orderdetails d on o.orderNumber = d.orderNumber group by o.customerNumber having total < 50000`

- using aggregate `$group` , `$sum`, `$multiply`, `$lookup`, `$match`

::left::

```js
    // Aggregate $group, $sum, $multiply, $lookup, $match
    ex24: async function (client) {
        const db = client.db('pg_classic')
        const orderdetails = db.collection('orderdetails')
        const embedded_pl = [{ "$match": { "$expr": { 
            "$eq": ["$ordernumber", "$$o_no"] } } }]
        const findResult = await orderdetails.aggregate([
            {
                "$lookup": {
                    "from": "orders",
                    "let": { "o_no": "$ordernumber" },
                    "pipeline": embedded_pl,
                    "as": "order_details"
                }
            },
```
::right::

```js

            { "$unwind": "$order_details" }, 
            // match field must begin with $
            { "$addFields": { 
                "customernumber": 
                "$order_details.customernumber" } }, 
            { "$group": { "_id": "$customernumber", 
            "total": { "$sum": { "$multiply": 
            ["$priceeach", "$quantityordered"] } } } },
            { "$match": { "total": { "$lt": 
            new Decimal128("50000") } } },
            { "$sort": { "_id": 1 } } // ascending
        ])
        for await (const product of findResult) {
            console.log(product);
        }
    },
```
::default::


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