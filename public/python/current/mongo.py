from pymongo import MongoClient
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
try:
    database = client.get_database("classic")
    offices_collection = database.get_collection("offices")
    # query = {"city": "San Francisco"}
    # offices_cursor = offices_collection.find(query)
    # office_lists = offices_cursor.to_list()
    # for i in range(len(office_lists)):
    #     print(office_lists[i])
    
    pipeline = [{
        "$lookup":{
            "from": "employees",
            "localField": "officeCode",
            "foreignField": "officeCode",
            "as": "employees"
        },
    },{
        "$match":{
            "employees.officeCode": "7"
        }
    },{
        "$project":{
            "officeCode":1,
            "city":1,
            "country":1,
            "employees.employeeNumber": 1,
            "employees.firstName": 1,
            "employees.lastName": 1
        }
    }]
    office_employee_cursor = offices_collection.aggregate(pipeline=pipeline)
    # for office in office_employee_cursor:
    #     print(office["officeCode"])
    #     for employee in office["employees"]:
    #         print(employee["employeeNumber"])
    for office in office_employee_cursor:
        print(office)
    
    client.close()
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)

