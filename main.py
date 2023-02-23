from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from mongoengine import connect
import json
import pymongo
from bson.objectid import ObjectId

app = FastAPI()

connect(db="test", host="localhost", port=27017)


@app.get("/")
def home():
    return {"message":"Hello World!"} 

#Ancienne version avec mongoengine
#@app.get("/get_all_tests")
#def get_all_tests():
#    tests_list = json.loads(Test.objects().to_json())
#    return{"tests": tests_list}


@app.get("/get_test")
def get_test():
    
    myTests = pymongo.MongoClient('localhost', 27017)
    dataBase = myTests["test"]
    collection = dataBase["test"]
    #print(list(collection.find({},{"_id":0})))
    x = jsonable_encoder(list(collection.find({},{"_id":0})))
    return JSONResponse(content=x)



@app.delete("/delete_test")
def delete_test(age: str):
    myTests = pymongo.MongoClient('localhost', 27017)
    dataBase = myTests["test"]
    collection = dataBase["test"]
    myQuery = {'age':age}
    collection.delete_one(myQuery)

@app.post("/add_test")
def add_test(nom: str, age: str, loisir: str):
    myTests = pymongo.MongoClient('localhost', 27017)
    dataBase = myTests["test"]
    collection = dataBase["test"]
    myQuery = {'nom':nom, 'age':age, 'loisir': loisir}
    collection.insert_one(myQuery)
    
@app.put("/update_test")
def update_test(oldname: str, nom: str,age: str,loisir: str):
    myTests = pymongo.MongoClient("localhost", 27017)
    dataBase = myTests["test"]
    collection = dataBase["test"]
    myOldQuery = {"nom":oldname}
    myQuery = {"$set":{"nom":nom, "age": age, "loisir": loisir}}
    collection.update_one(myOldQuery,myQuery)
    return{"test_supp":get_test()}
