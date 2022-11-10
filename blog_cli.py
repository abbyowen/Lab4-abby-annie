from pymongo import MongoClient                          # mongodb connector
import os
from shlex import split
import sys

###### on_startup ######
# Displays message when the program is started
def on_startup():
    print("Hello, welcome to our blog!")

###### db_connect ######
# Connect to the database and return the cursor for executing queries and the connection for closing
def db_connect():
    # load database
    MONGO_PASS = os.getenv('MONGO_PASSWORD')
    server = f"mongodb+srv://abbyhaowen:{MONGO_PASS}@cluster0.ikskh8p.mongodb.net/test"
    client = MongoClient(server)
    db = client["cosc61-lab3"]
    zipcodes = db["zipcodes"]
    print("connection established")
    return db, zipcodes

###### read_input ######
def read_input(input, db, collection):
     # split input by space
    words = split(input)

    # register user
    if words[0] == "post": 
        print("posting")

###### run ######   
# Main functionality, gets stdin and calls read_input to parse input    
def run():
    # Display start message
    on_startup()
    db, collection = db_connect()

    for line in sys.stdin:
        if 'logout' == line.rstrip():
            break
        else:
            read_input(line, db, collection)
    
    
    print("goodbye!") 
   
if __name__ == '__main__':
    run()
