#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import web
import couchdb
import json

urls = (
    '/GetNewsById/(.*)', 'getnewsbyid',
    '/GetLastNews/(.*)', 'getlastnews',
    '/GetPressNews/(.*)', 'getpressnews',
    '/SearchNews/(.*)', 'searchnews',
)
app = web.application(urls, globals())


class getnewsbyid:
    def GET(self, news_id):
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']

        y = ""
        for id in db:

            doc = db[id]
            x = json.dumps(doc)
            if doc['newsId'] == news_id:
                y = x

        return y


class getlastnews:
    def GET(self, num):
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']
        count = 0
        y = ""

        for id in db:
            doc = db[id]
            x = json.dumps(doc)
            y = y + x + ','
            count += 1
            if count == int(num):
                break
        b = "[" + y + "]"
        b = b.replace(',]', ']', 1)
        return b


class getpressnews:
    def GET(self, pub_name):
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']
        y = ""
        x = ""
        for id in db:

            doc = db[id]
            x = json.dumps(doc)
            if doc['press'] == pub_name:
                y = y + x + ','

        b = "[" + y + "]"
        b = b.replace(',]', ']', 1)
        return b


class searchnews:
    def GET(self, search_word):

        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']

        y = ""

        for id in db:

            doc = db[id]
            x = json.dumps(doc)
            if set(search_word.split()) & set(doc['text'].split()):
                y = y + x + ','

        b = "[" + y + "]"
        b = b.replace(',]', ']', 1)

        return b


if __name__ == "__main__":
    app.run()
