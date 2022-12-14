import re
from datetime import datetime

def post(posts, blogs, name, user, title, postBody, tags, time):
    # check if blog name exists in db
    permalink  = name+'.'+re.sub('[^0-9a-zA-Z]+', '_', title)
    res = blogs.find({"blogName": name}, {"limit":1})
    if len(list(res)) == 0:
        print("New blog created!")
        blog = {'blogName': name, "posts": []}
        blogs.insert_one(blog) 
        
    r = {'permalink': permalink, 'user': user, 'title': title, 'postBody': postBody, 'tags': tags, 'timestamp': time, 'comments': []}
    posts.insert_one(r)
    blogs.update_one({"blogName": name}, {"$push": {"posts": permalink}})


def comment(posts, comments, name, permalink, user, commentBody, timestamp):
    comment_permalink  = name+'.'+re.sub('[^0-9a-zA-Z]+', '_', timestamp)
    post_res = posts.find({"permalink": permalink}, {"limit":1})
    if len(list(post_res)) != 0:
        insert_comment = {"permalink": comment_permalink, "user": user, "commentBody": commentBody, "timestamp": timestamp, "comments": []}
        comments.insert_one(insert_comment)
        # insert into the post 
        posts.update_one({"permalink": permalink}, {"$push": {"comments": comment_permalink}})
        
    else:
        comment_res = comments.find({"permalink": permalink}, {"limit":1})
        if len(list(comment_res)) != 0:
            insert_comment = {"permalink": comment_permalink, "user": user, "commentBody": commentBody, "timestamp": timestamp, "comments": []}
            comments.insert_one(insert_comment)
            # insert into the post 
            comments.update_one({"permalink": permalink}, {"$push": {"comments": comment_permalink}})
        else:
            print("permalink specified does not exist. please try again with an existing permalink to a comment or post.")

def print_post(blog):
    print("-----------------")
    title = blog["title"]
    user = blog["user"]
    timestamp = str(blog["timestamp"])
    permalink = blog["permalink"]
    body =  blog["postBody"]
    tags = blog["tags"]
    if tags == "":
        string = f"title: {title}\nuserName: {user}\ntimestamp: {timestamp}\npermalink: {permalink}\nbody: {body}"
    else:
        string = f"title: {title}\nuserName: {user}\ntags: {tags}\ntimestamp: {timestamp}\npermalink: {permalink}\nbody: {body}"

    print(string)

def single_comment_print(c, depth):
    
    user = c["user"]
    permalink = c["permalink"]
    body = c["commentBody"]
    padding = ""
    for i in range(depth):
        padding += "\t"
    string = f"{padding}user: {user}\n{padding}permalink: {permalink}\n{padding}comment: {body}"
    print(padding + "-----------------")
    print(string)

def print_comments(comments, clist, depth):
    if clist == []:
        return
    else:
        for link in clist: 
            pipeline = [
                {"$match": {"permalink": link}}, 
                {"$project": {"_id":0}}
            ]
            one_comment = comments.aggregate(pipeline)
            
            for res in one_comment:
                single_comment_print(res, depth)
                print_comments(comments, res["comments"], depth + 1)

def show(blogs, posts, comments, name):
    
    check_exists = blogs.find({"blogName": name}, {"limit": 1})
    if len(list(check_exists)) != 0:
        post_permalinks = blogs.find({"blogName": name})
        for post in post_permalinks:
            for p in post["posts"]:
                pipeline = [
                    {"$match": {"permalink": p}}, 
                    {"$project": {"_id":0}}
                ]
                
                body = posts.aggregate(pipeline)
                for res in body:
                    print_post(res)
                    clist = res["comments"]
                    print_comments(comments, clist, 1)
    else:
        print("no blog with supplied name")
                
                       
def delete(posts, comments, permalink, username, timestamp):
    res = posts.find({"permalink":permalink}, {"limit": 1})
    res2 = comments.find({"permalink": permalink}, {"limit": 1})

    # test line: 
    if len(list(res)) != 0:
        posts.update_one({"permalink": permalink},{"$set":{"timestamp":timestamp,"postBody":f"deleted by {username}"}})
        print("post deleted")
    elif len(list(res2)) != 0:
        print("hello")
        comments.update_one({f"permalink": permalink},{"$set":{"timestamp":timestamp,"commentBody":f"deleted by {username}"}})
        print("comments deleted")
    else:
        print("error")

def single_comment_print_for_search(c, search_query, depth):
    user = c["user"]
    permalink = c["permalink"]
    body = f"comment contents containing {search_query}"
    padding = ""
    for i in range(depth):
        padding += "\t"
    string = f"{padding}user: {user}\n{padding}permalink: {permalink}\n{padding}comment: {body}"
    print("-----------------")
    print(string)

def print_post_for_search(post, search_query):
    print("-----------------")
    title = post["title"]
    user = post["user"]
    timestamp = str(post["timestamp"])
    permalink = post["permalink"]
    body = f"body contents containing {search_query}"
    tags = post["tags"]
    if tags == "":
        string = f"title: {title}\nuserName: {user}\ntimestamp: {timestamp}\npermalink: {permalink}\nbody: {body}"
    else:
        string = f"title: {title}\nuserName: {user}\ntags: {tags}\ntimestamp: {timestamp}\npermalink: {permalink}\nbody: {body}"

    print(string)

def print_comments_for_search(comments, clist, search_query, depth):
    if clist == []:
        return
    else:
        for link in clist: 
            pipeline = [
                {"$match": {"permalink": link}}, 
                {"$project": {"_id":0}}
            ]
            one_comment = comments.aggregate(pipeline)
            
            for res in one_comment:
                if res["commentBody"] == search_query:
                    single_comment_print_for_search(res, search_query, depth)
                    print_comments_for_search(comments, res["comments"], search_query, depth + 1)
                else:
                    print_comments_for_search(comments, res["comments"], search_query, depth)

def search(blogs, posts, comments, blogname, search_query):
    post_permalinks = blogs.find({"blogName": blogname})
    for post in post_permalinks:
        for p in post["posts"]:
            pipeline = [
                {"$match": {"permalink": p}}, 
                {"$project": {"_id":0}}
            ]
            
            post = posts.aggregate(pipeline)
            for res in post:
                post_body = res["postBody"]
    
                tags = res["tags"]
                found = False
                if post_body == search_query:
                    print_post_for_search(res, search_query)
                    found = True
                if tags == search_query:
                    print_post_for_search(res, search_query)
                    found = True
                clist = res["comments"]
                if found:
                    print_comments_for_search(comments, clist, search_query, 1)
                else:
                    print_comments_for_search(comments, clist, search_query, 0)
                found = False
                




def clear(posts, comments, blogs):
    posts.delete_many({})
    comments.delete_many({})
    blogs.delete_many({})
    print("databases clear!")


        

