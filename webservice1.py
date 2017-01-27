#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys

import web
import couchdb
import json 
import math   

urls = (
    '/GetNewsById/(.*)','getnewsbyid',
    '/GetLastNews/(.*)', 'getlastnews',
    '/GetPressNews/(.*)', 'getpressnews',
    )
app = web.application(urls, globals())

class getnewsbyid:
    def GET(self, news_id):
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']    
        
        
        y=""
        for id in db:    
            
            doc=db[id]
            x=json.dumps(doc)
            if doc['newsId']==news_id:
                y=x 
                
        return y




class getlastnews:        
    def GET(self, num):
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']
        count=0
        y=""
        
    
            
        for id in db:
            doc=db[id]
            x=json.dumps(doc)
            y=y+x+',' 
            count=count+1
            if count==int(num):
                break   
        return "["+y+"]"
    
    
    
class getpressnews:        
    def GET(self, pub_name):
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']
        y=""
        x=""
        for id in db:    
            
            doc=db[id]
            x=json.dumps(doc)
            if doc['press']==pub_name:
                y=y+x+',' 
        
        
        return "["+y+"]"   
        


if __name__ == "__main__":
    app.run()