#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import web
import json
from user_define_classes import DnsServer
from user_define_classes import Server

server_dns = DnsServer('192.168.37.4', 5984)
server0 = Server('192.168.37.4', 5984)
server1 = Server('192.168.37.5', 5984)
server2 = Server('192.168.37.6', 5984)

server0.couch_server.replicate("news",
                               server1.get_news_database_address(),
                               continuous=True)

server1.couch_server.replicate("news",
                               server2.get_news_database_address(),
                               continuous=True)

server2.couch_server.replicate("news",
                               server0.get_news_database_address(),
                               continuous=True)

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

        dns_db = server_dns.get_dns_database()
        if news_id in dns_db:
            doc_place = dns_db[news_id]
            address = doc_place['address']
            backup_address = doc_place['backup_address']
            db = None
            if (server0.is_this_server(address) or server0.is_this_server(backup_address)) and server0.is_available():
                db = server0.get_news_database()
            elif (server1.is_this_server(address) or server1.is_this_server(backup_address)) and server1.is_available():
                db = server1.get_news_database()
            elif (server2.is_this_server(address) or server2.is_this_server(backup_address)) and server2.is_available():
                db = server2.get_news_database()

            doc = db[news_id]
            return json.dumps(doc)
        else:
            return ""


class GetLastNews:
    def __init__(self):
        pass

    def GET(self, num):
        db = server0.get_news_database()
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
            db = server0.get_news_database()

            for _id in db:
                news = db[_id]
                if news['press'] == pub_name:
                    array_news.append(news)
        except:
            error = "server 0 is crashed"

        try:
            db = server1.get_news_database()
            for _id in db:
                news = db[_id]
                if news['press'] == pub_name:
                    array_news.append(news)
        except:
            error = "server 1 is crashed"

        try:
            db = server2.get_news_database()

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
            db = server0.get_news_database()
            for _id in db:
                news = db[_id]
                if set(search_word.split()) & set(news['text'].split()):
                    array_news.append(news)
        except:
            error = "server 0 is crashed"

        try:
            db = server1.get_news_database()
            for _id in db:
                news = db[_id]
                if set(search_word.split()) & set(news['text'].split()):
                    array_news.append(news)
        except:
            error = "server 1 is crashed"

        try:
            db = server2.get_news_database()
            for _id in db:
                news = db[_id]
                if set(search_word.split()) & set(news['text'].split()):
                    array_news.append(news)
        except:
            error = "server 2 is crashed"

        return json.dumps(array_news, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    app.run()
