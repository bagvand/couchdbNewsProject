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

servers = [
    server0,
    server1,
    server2
]

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
            db = None

            for server in servers:
                if server.is_this_server(address):
                    if server.is_available():
                        db = server.get_news_database()
                    elif server.backup_server.is_available():
                        db = server.backup_server.get_news_database()
                    break

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

        for server in servers:
            db = server.get_news_database()
            if db is not None:
                for _id in db:
                    news = db[_id]
                    if news['press'] == pub_name:
                        array_news.append(news)

        return json.dumps(array_news, indent=4, sort_keys=True, ensure_ascii=False)


class SearchNews:
    def __init__(self):
        pass

    def GET(self, search_word):

        array_news = []

        for server in servers:
            db = server.get_news_database()
            if db is not None:
                for _id in db:
                    news = db[_id]
                    if set(search_word.split()) & set(news['text'].split()):
                        array_news.append(news)

        return json.dumps(array_news, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    app.run()
