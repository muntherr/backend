from pymongo.mongo_client import MongoClient
from flask_pymongo import pymongo

uri = "mongodb+srv://muntheranati:testclus@trainingcluster.ejwnjgh.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = pymongo.MongoClient(uri)

db = client.get_database("School-managmenet")
