const { Decimal128 } = require('mongodb');
module.exports = {
    // Create Collection and Document
    ex1: async function (client) {
        const db = client.db('my_mongo')
        const users = db.collection('users')
        const result = await users.insertOne({ "username": "Alice", "email": "alice@gmail.com" })
        console.log(`A document was inserted with the _id: ${result.insertedId}`);
    },
    // Drop database
    ex2: async function (client) {
        const db = client.db('my_mongo')
        await db.dropDatabase();
    },
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
    },
    // Insert many documents
    ex4: async function (client) {
        const db = client.db('my_mongo')
        const users = db.collection('users')
        const insertManyresult = await users.insertMany([{ "username": "Alice", "email": "alice@gmail.com" }, { username: 'Jack', email: 'jack@gmail.com' }])
        let ids = insertManyresult.insertedIds;
        console.log(`${insertManyresult.insertedCount} documents were inserted.`);
        for (let id of Object.values(ids)) {
            console.log(`Inserted a document with id ${id}`);
        }
    },
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
    // Find excact match
    ex6: async function (client) {
        const db = client.db('my_mongo')
        const users = db.collection('users')
        const findResult = await users.find({ username: 'Jack' })
        for await (const doc of findResult) {
            console.log(doc);
        }
    },
    // Comparison Operators
    ex7: async function (client) {
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
    },
    // Logical Operators
    ex8: async function (client) {
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
    },
    // Expression Operator
    ex9: async function (client) {
        const db = client.db('pg_classic')
        const products = db.collection('products')
        const findResult = await products.find({ $expr: { $lt: ["$buyprice", "$msrp"] } })
        for await (const doc of findResult) {
            console.log(doc.productcode, doc.buyprice, doc.msrp);
        }
    },
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
            console.log(doc.ordernumber, Number(doc.priceeach), doc.quantityordered, Number(doc.priceeach) * doc.quantityordered);
        }
    },
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
    },
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
    },
    // Projection
    ex13: async function (client) {
        const db = client.db('pg_classic')
        const customers = db.collection('customers')
        const findResult = await customers.find({}).project({ "_id": false })
        for await (const doc of findResult) {
            console.log(doc._id, doc.customernumber, doc.customername);
        }
    },
    // Limit and Skip
    ex14: async function (client) {
        const db = client.db('pg_classic')
        const customers = db.collection('customers')
        const findResult = await customers.find({}).project({ "_id": false }).limit(5).skip(5)
        for await (const doc of findResult) {
            console.log(doc.customernumber, doc.customername);
        }
    },
    // Sort
    ex15: async function (client) {
        const db = client.db('pg_classic')
        const customers = db.collection('customers')
        const findResult = await customers.find({}).project({ "_id": false }).limit(5).sort({ 'customernumber': 'desc' })
        for await (const doc of findResult) {
            console.log(doc.customernumber, doc.customername);
        }
    },
    // Count
    ex16: async function (client) {
        const db = client.db('pg_classic')
        const customers = db.collection('customers')
        const countUSACustomers = await customers.countDocuments({ "country": "USA" })
        console.log(`Total customer in USA = ${countUSACustomers}`)
    },
    // Distinct
    ex17: async function (client) {
        const db = client.db('pg_classic')
        const orders = db.collection('orders')
        const findResult = await orders.distinct('customernumber')
        for (const customernumber of findResult) {
            console.log(customernumber);
        }
    },
    // Aggregate $match
    ex18: async function (client) {
        const db = client.db('pg_classic')
        const products = db.collection('products')
        const findResult = await products.aggregate([{ "$match": { "productline": "Motorcycles", "buyprice": { "$lt": new Decimal128('60') } } }])
        for await (const product of findResult) {
            console.log(product);
        }
    },
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
    },
    // Aggreate $lookup, $project
    ex20: async function (client) {
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
            { "$project": { productcode: true, quantityordered: true, "product_order.productname": true, "product_order.buyprice": true, "product_order.productline": true, _id: false } },
        ])
        for await (const product of findResult) {
            console.log(product);
        }
    },
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
            { "$project": { productcode: true, quantityordered: true, "product_order.productname": true, "product_order.buyprice": true, "product_order.productline": true, _id: false } },
        ])
        for await (const product of findResult) {
            console.log(product);
        }
    },
    // Aggreate $lookup, $project, $unwind
    ex22: async function (client) {
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
            { "$addFields": { "productname": "$product_order.productname", "buyprice": "$product_order.buyprice", "productline": "$product_order.productline" } }, // match field must begin with $
            { "$project": { productcode: true, quantityordered: true, "productname": true, "buyprice": true, "productline": true, _id: false } },
        ])
        for await (const product of findResult) {
            console.log(product);
        }
    },
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
    // Aggregate $group, $sum, $multiply, $lookup, $match
    ex24: async function (client) {
        const db = client.db('pg_classic')
        const orderdetails = db.collection('orderdetails')
        const embedded_pl = [{ "$match": { "$expr": { "$eq": ["$ordernumber", "$$o_no"] } } }]
        const findResult = await orderdetails.aggregate([
            {
                "$lookup": {
                    "from": "orders",
                    "let": { "o_no": "$ordernumber" },
                    "pipeline": embedded_pl,
                    "as": "order_details"
                }
            },
            { "$unwind": "$order_details" }, // match field must begin with $
            { "$addFields": { "customernumber": "$order_details.customernumber" } }, // match field must begin with $
            { "$group": { "_id": "$customernumber", "total": { "$sum": { "$multiply": ["$priceeach", "$quantityordered"] } } } },
            { "$match": { "total": { "$lt": new Decimal128("50000") } } },
            { "$sort": { "_id": 1 } } // ascending
        ])
        for await (const product of findResult) {
            console.log(product);
        }
    },
} 