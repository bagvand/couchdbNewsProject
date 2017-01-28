#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import json
from user_define_classes import DnsServer
from user_define_classes import Server

server_dns = DnsServer('192.168.37.4', 5984)
server0 = Server('192.168.37.4', 5984)
server1 = Server('192.168.37.5', 5984)
server2 = Server('192.168.37.6', 5984)

rond = 0
for root, dirs, files in os.walk('news/', topdown=False):
    for name in files:
        print(os.path.join(root, name))
        one_file = open(os.path.join(root, name), 'r')
        array_news = json.loads(one_file.read(), "utf8")
        for news in array_news:
            _id = news['id']
            del news['id']
            if _id not in server_dns.get_news_database():
                flag = 0
                if not server0.is_available():
                    rond = (rond + 1) % 3
                elif rond == 0 and server0.is_available() and flag == 0:
                    server0.get_news_database()[_id] = news
                    server_dns.get_dns_database()[_id] = {"address": server0.get_server_address(),
                                                          "backup_address": server1.get_server_address()}
                    rond = (rond + 1) % 3
                    flag = 1
                elif not server1.is_available():
                    rond = (rond + 1) % 3
                elif rond == 1 and server1.is_available() and flag == 0:
                    server1.get_news_database()[_id] = news
                    server_dns.get_dns_database()[_id] = {"address": server1.get_server_address(),
                                                          "backup_address": server2.get_server_address()}
                    rond = (rond + 1) % 3
                    flag = 1
                elif not server2.is_available():
                    rond = (rond + 1) % 3

                elif rond == 2 and server2.is_available() and flag == 0:
                    server2.get_news_database()[_id] = news
                    server_dns.get_dns_database()[_id] = {"address": server2.get_server_address(),
                                                          "backup_address": server0.get_server_address()}
                    rond = (rond + 1) % 3
                    flag = 1

            else:
                is_update_exist = False
                doc_place = server_dns.get_dns_database()[_id]
                address = doc_place['address']
                backup_address = doc_place['backup_address']
                news_inDb = None

                db = None
                if server0.is_this_server(address) and server0.is_available():
                    db = server0.get_news_database()
                elif server1.is_this_server(address) and server1.is_available():
                    db = server1.get_news_database()
                elif server2.is_this_server(address) and server2.is_available():
                    db = server2.get_news_database()

                news_inDb = db[_id]
                for key in news.keys():
                    if news[key] != news_inDb.get(key):
                        news_inDb[key] = news[key]
                        is_update_exist = True

                if is_update_exist:
                    db[news_inDb.id] = news_inDb
