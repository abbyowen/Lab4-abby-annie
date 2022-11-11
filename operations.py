import re

def post(collection, name, user, title, postBody, tags, time):
    # check if blog name exists in db
    permalink  = name+'.'+re.sub('[^0-9a-zA-Z]+', '_', title)
    res = collection.find({"blogName": name}, {"limit":1})
    if len(list(res)) == 0:
        print("nothing!") 
        r = {'blogName': name, 'posts': [{'permalink': permalink, 'user': user, 'title': title, 'postBody': postBody, 'tags': tags, 'time': time, 'comments': []}]}
        collection.insert_one(r)
        check = collection.find({"blogName": name})
        for x in check: 
            print(x)
    else:
        r = {'permalink': permalink, 'user': user, 'title': title, 'postBody': postBody, 'tags': tags, 'time': time, 'comments': []}
        collection.update_one({ "blogName": name },{ "$push": { "posts": r } })
        check = collection.find({"blogName": name})
        for x in check: 
            print(x)


def comment(collection, name, link, user, commentBody, timestamp):
    collection.aggregate({"match": {"blogName": name}}, {"match": {"posts.permalink": link}})

        

