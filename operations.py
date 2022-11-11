import re
from datetime import datetime

def post(posts, blogs, name, user, title, postBody, tags, time):
    # check if blog name exists in db
    permalink  = name+'.'+re.sub('[^0-9a-zA-Z]+', '_', title)
    res = blogs.find({"blogName": name}, {"limit":1})
    if len(list(res)) == 0:
        
        print("New blog created!")
        blog = {'blogName': name}
        blogs.insert_one(blog) 
        
    r = {'title': title, 'permalink': permalink, 'user': user, 'title': title, 'postBody': postBody, 'tags': tags, 'time': time, 'comments': []}
    posts.insert_one(r)
    check = posts.find({"permalink": permalink})
    for x in check: 
        print(x)

def delete(posts, comments, permalink, username):
    res = posts.find({"permalink":permalink})
    res2 = comments.find({"permalink": permalink})

    # test line: 
    if res:
        posts.update_one({"permalink": permalink},{"$set":{"timestamp":datetime.now(),"postBody":"deleted by {username}"}})
        print("post deleted")
    elif res2:
        comments.update_one({"permalink": permalink},{"$set":{"timestamp":datetime.now(),"postBody":"deleted by {username}"}})
        print("comments deleted")
    else:
        print("error")


        

