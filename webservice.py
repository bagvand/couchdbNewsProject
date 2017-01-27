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
        if news_id in db:
            return db[news_id]
        else:
            return ""


class getlastnews:
    def GET(self, num):
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']
        count = 0
        array_news = []

        for _id in db:
            news = db[_id]
            array_news.append(news)
            count += 1
            if count == int(num):
                break
        return json.dump(array_news)


class getpressnews:
    def GET(self, pub_name):
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']
        array_news = []

        for _id in db:
            news = db[_id]
            if news['press'] == pub_name:
                array_news.append(news)

        return json.dump(array_news)


class searchnews:
    def GET(self, search_word):

        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']
        array_news = []

        for _id in db:

            news = db[_id]
            if set(search_word.split()) & set(news['text'].split()):
                array_news.append(news)

        return json.dump(array_news)


if __name__ == "__main__":
    app.run()
