import re

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


        

