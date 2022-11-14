from pymongo import MongoClient                          # mongodb connector
import os
from configparser import ConfigParser
from shlex import split
import sys
from operations import *
from datetime import datetime

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

    if words[0] == "post" and (len(words) == 6 or len(words) == 7): 
        name = words[1]
        user = words[2]
        title = words[3]
        body = words[4]
        tags = words[5]
        if len(words) == 6:
            time = datetime.now()
        elif len(words) == 6:
            time = words[6]
        post(posts, blogs, name, user, title, body, tags, time)
        print("posting")
    elif words[0] == "comment" and (len(words) == 5 or len(words) == 6):
        name = words[1]
        link = words[2]
        user = words[3]
        body = words[4]
        if len(words) == 5:
            time = str(datetime.now())
        elif len(words) == 6:
            time = words[5]
        comment(posts, comments, name, link, user, body, time)
        print("commenting")
    elif words[0] == "delete" and (len(words) == 4 or len(words) == 5):
        # delete blogname permalink userName timestamp
        if len(words) == 4:
            timestamp = str(datetime.now())
        elif len(words) == 5:
            timestamp = words[4]
        
        blogname = words[1]
        permalink = words[2]
        username = words[3]
        name_check = permalink.split('.')[0]
        if name_check != blogname:
            print("blog name and permalink do not match")
            return
        delete(posts, comments, permalink, username, timestamp)
        print("deleting")
    elif words[0] == "show" and len(words) == 2:
        print("showing")
        name = words[1]
        print(f"in {name}:")
        show(blogs, posts, comments, name)
    elif words[0] == "search" and len(words) == 3:
        print("searching")
        blogname = words[1]
        search_query = words[2]
        search(blogs, posts, comments, blogname, search_query)
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
