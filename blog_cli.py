from pymongo import MongoClient                          # mongodb connector
import os
from configparser import ConfigParser
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
    parser = ConfigParser()
    parser.read("config.ini")
    username = parser.get('mongo','username')
    password = parser.get('mongo','password')
    server = "mongodb+srv://{username}:{password}@cluster0.rbot07u.mongodb.net/test"
    client = MongoClient(server)
    db = client["lab4"]
    zipcodes = db["posts"]
    print("connection established")
    return db, zipcodes

###### read_input ######
def read_input(input, db, collection):
     # split input by space
    words = split(input)

    if words[0] == "post": 
        print("posting")
    elif words[0] == "comment":
        print("commenting")
    elif words[0] == "delete":
        print("deleting")
    elif words[0] == "show":
        print("showing")


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
