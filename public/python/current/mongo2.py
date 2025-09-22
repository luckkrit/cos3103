from pymongo import MongoClient
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
try:
    db = client['classic']
    customers = db.customers
    client.close()
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)

