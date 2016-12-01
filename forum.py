
from flask import Flask, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import json
import time

app = Flask(__name__)
CORS(app)

class Post():
    def __init__(self,user,text):
        self.created=time.time()
        self.user=user
        self.text=text

    def __repr__(self):
        return str(self.__dict__)

class Thread():
    def __init__(self,title,user,text):
        self.created=time.time()
        self.title=title
        self.user=user
        self.text=text
        self.posts=[]

    def insertPost(self,post):
        self.posts.append(post)

    def countReplys(self):
        return len(self.posts)

    def lastPoster(self):
        return self.posts[-1].user.name

    def getPosts(self):
        return self.posts

class Forum():
    def __init__(self):
        self.threads=[]

    def addThread(self,title,user,text):
        self.threads.append(Thread(title,user,text))
        return self.threads[-1].created

    def listThreads(self):
        list=[]
        for t in self.threads:
            d={}
            d['title'] = t.title
            d['created'] = t.created
            list.append(d)
        return list

    def getThread(self,created):
        for t in self.threads:
            if t.created == float(created):
                return (t.__dict__)
        return 0

    def addPost(self, created,user,text):
        for t in self.threads:
            if t.created == float(created):
                t.posts.append(Post(user,text))
                return 1
        return 0


f=Forum()


@app.route('/list',methods = ['GET'])
def list():
    return (str(f.listThreads()))

@app.route('/<created>',methods = ['GET'])
def thread(created):
    return (str(f.getThread(created)))
	
@app.route('/addthread/',methods = ['POST'])
def addThread():
    data=eval(request.get_data())
    f.addThread(data[0],data[1],data[2])
    return ("OK")

@app.route('/addpost/',methods = ['POST'])
def addPost():
    data=eval(request.get_data())
    f.addPost(data[0],data[1],data[2])
    return ("OK")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1201)
