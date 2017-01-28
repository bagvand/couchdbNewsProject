#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import web
import couchdb
import json

urls = (
    '/GetNewsById/(.*)', 'GetNewsById',
    '/GetLastNews/(.*)', 'GetLastNews',
    '/GetPressNews/(.*)', 'GetPressNews',
    '/SearchNews/(.*)', 'SearchNews',
)
app = web.application(urls, globals())


class GetNewsById:
    def __init__(self):
        pass

    def GET(self, news_id):
        dns_couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        dns_db = dns_couch['dns']

        if news_id in dns_db:
            doc = dns_db[news_id]
            ip = doc['ip']
            ip_b = doc['backup']
            try:
                couch = couchdb.Server('http://admin:admin@' + ip + ':5984/')

            except:
                couch = couchdb.Server('http://admin:admin@' + ip_b + ':5984/')

            db = couch['news']
            doc = db[news_id]
            return json.dumps(doc)
        else:
            return ""


class GetLastNews:
    def __init__(self):
        pass

    def GET(self, num):
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['news']
        count = 0
        array_news = []

        for _id in db:
            news = db[_id]
            array_news.append(news)
            count += 1
            print news
            if count == int(num):
                break
        return json.dumps(array_news, indent=4, sort_keys=True, ensure_ascii=False)


class GetPressNews:
    def __init__(self):
        pass

    def GET(self, pub_name):
        array_news = []
        try:
            couch = couchdb.Server('http://admin:admin@192.168.37.4:5984/')
            db = couch['news']

            for _id in db:
                news = db[_id]
                if news['press'] == pub_name:
                    array_news.append(news)
        except:
            error = "server 1 is crashed"

        try:
            couch = couchdb.Server('http://admin:admin@192.168.37.5:5984/')
            db = couch['news']

            for _id in db:
                news = db[_id]
                if news['press'] == pub_name:
                    array_news.append(news)
        except:
            error = "server 2 is crashed"

        try:
            couch = couchdb.Server('http://admin:admin@192.168.37.6:5984/')
            db = couch['news']

            for _id in db:
                news = db[_id]
                if news['press'] == pub_name:
                    array_news.append(news)
        except:
            error = "server 2 is crashed"

        return json.dumps(array_news, indent=4, sort_keys=True, ensure_ascii=False)


class SearchNews:
    def __init__(self):
        pass

    def GET(self, search_word):

        array_news = []

        try:
            couch = couchdb.Server('http://admin:admin@192.168.37.4:5984/')
            db = couch['news']
            for _id in db:
                news = db[_id]
                if set(search_word.split()) & set(news['text'].split()):
                    array_news.append(news)
        except:
            error = "server 1 is crashed"

        try:
            couch = couchdb.Server('http://admin:admin@192.168.37.5:5984/')
            db = couch['news']
            for _id in db:
                news = db[_id]
                if set(search_word.split()) & set(news['text'].split()):
                    array_news.append(news)
        except:
            error = "server 1 is crashed"

        try:
            couch = couchdb.Server('http://admin:admin@192.168.37.6:5984/')
            db = couch['news']
            for _id in db:
                news = db[_id]
                if set(search_word.split()) & set(news['text'].split()):
                    array_news.append(news)
        except:
            error = "server 1 is crashed"

        return json.dumps(array_news, indent=4, sort_keys=True, ensure_ascii=False)


class replicate:
    def GET(self, password):
        count = 0
        if password == "123456":
            couch = couchdb.Server()

            try:
                couch.replicate('http://admin:admin@192.168.37.4:5984/news',
                                'http://admin:admin@192.168.37.5:5984/news', continuous=True)
                count = count + 1
            except:
                error = "error"

            try:
                couch.replicate('http://admin:admin@192.168.37.5:5984/news',
                                'http://admin:admin@192.168.37.6:5984/news', continuous=True)
                count = count + 1
            except:
                error = "error"

            try:
                couch.replicate('http://admin:admin@192.168.37.6:5984/news',
                                'http://admin:admin@192.168.37.4:5984/news', continuous=True)
                count = count + 1
            except:
                error = "error"

        else:
            result = "password is not correct"

        result = count

        return result


if __name__ == "__main__":
    app.run()
