from pymongo import MongoClient
from datetime import datetime
import json

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# use database
db = client["adaptive_test"]

# collection
questions = db["questions"]

# documents to insert
with open("../questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# insert documents
questions.insert_many(data)

print("Questions inserted successfully!")