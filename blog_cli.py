from pymongo import MongoClient                          # mongodb connector
import os
from dotenv import load_dotenv

MONGO_PASS = os.getenv('MONGO_PASSWORD')
server = f"mongodb+srv://abbyhaowen:{MONGO_PASS}@cluster0.ikskh8p.mongodb.net/test"
client = MongoClient(server)
db = client["cosc61-lab3"]
zipcodes = db["zipcodes"]
print("established")