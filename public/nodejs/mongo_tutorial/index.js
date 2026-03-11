const { MongoClient } = require('mongodb');
const tutorial = require('./tutorial')

async function runGetStarted() {
    // Replace the uri string with your connection string
    const uri = 'mongodb://localhost:27017/';
    const client = new MongoClient(uri);
    await tutorial.ex24(client);
    try {
    } finally {
        await client.close();
    }
}
runGetStarted().catch(console.dir);