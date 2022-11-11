from pymongo import MongoClient                          # mongodb connector
import os
from configparser import ConfigParser
from shlex import split
import sys
from operations import *

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
    server = f"mongodb+srv://{username}:{password}@cluster0.rbot07u.mongodb.net/test"
    client = MongoClient(server)
    db = client["lab4"]
    posts = db["posts"]
    blogs = db["blogs"]
    comments = db["comments"]
    print("connection established")
    return db, posts, blogs, comments

###### read_input ######
def read_input(input, db, posts, blogs, comments):
    # split input by space
    # posts, blogs, comments are the collections
    words = split(input)

    if words[0] == "post" and len(words) == 7: 
        name = words[1]
        user = words[2]
        title = words[3]
        body = words[4]
        tags = words[5]
        time = words[6]
        post(posts, blogs, name, user, title, body, tags, time)
        print("posting")
    elif words[0] == "comment":
        print("commenting")
    elif words[0] == "delete":
        # delete blogname permalink userName timestamp
        blogname = words[1]
        permalink = words[2]
        username = words[3]
        timestamp = words[4]
        name_check = permalink.split('.')[0]
        if name_check != blogname:
            print("blog name and permalink do not match")
            return
        delete(posts, comments, permalink, username)
        print("deleting")
    elif words[0] == "show":
        print("showing")
    else:
        print("unknown input or invalid number of arguments")


###### run ######   
# Main functionality, gets stdin and calls read_input to parse input    
def run():
    # Display start message
    on_startup()
    db, posts, blogs, comments = db_connect()

    for line in sys.stdin:
        if 'logout' == line.rstrip():
            break
        else:
            read_input(line, db, posts, blogs, comments)
    
    
    print("goodbye!") 
   
if __name__ == '__main__':
    run()
