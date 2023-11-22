import pymongo
from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError
from bson.errors import InvalidId
# mongoLib/mongo.py

"""
This module is controlling the pi's database connection.
Please call the close function at the end.

Author: Diego Brandjes
Date:   05-10-2023
"""
class Mongo:

    # start database connection 
    def __init__(self, uri, database_name, collection_name):
        try:
            # Specify the connection URI with a timeout of 10 seconds
            print("Connecting to database. . .")
            self.client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=30000)
            
            # Access the specified database and collection
            db = self.client[database_name]
            self.card = db[collection_name]
            print("Connection to database successfull.")
        
        except ServerSelectionTimeoutError as e:
            # Handle connection timeout
            print(f"Connection to MongoDB timed out (30 seconds): {e}")
        
    # give it a variable to search for, will check if user exists. 
    def userExists(self, uid: str):
        try:
            criteria = {"_id": ObjectId(uid)}
            result = self.card.find_one(criteria)

            if result:
                self.user = result["_id"]
                self.beers = result['beers']

                if self.beers >= 1:
                    print(f"\nFound user: {self.user}, has {self.beers} drinks left\n")
                    return True
            
                elif self.beers <= 0:
                    print(f"User: {self.user} has no more drinks left.\n")
                    return False
                
            else:
                print("User not found.")
                return False

        except InvalidId:
            print("Invalid UID format")
            return False
        
    def decreaseBeer(self):
        try:
            if(self.beers >= 1):
                criteria = {"_id": ObjectId(self.user)}
                update_operation = {"$inc": {"beers": -1}}
                self.card.update_one(criteria, update_operation)

        except InvalidId:
            print("Invalid UID format")
            return False
        
    def closeConnection(self):
        print("Successfully closed database connection.")
        self.client.close()
    

  