#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import couchdb
import json

try:
    couch = couchdb.Server('http://admin:admin@192.168.37.4:5984/')
    if "news" in couch:
        db = couch['news']
    else:
        db = couch.create('news')
    avl_0 = 1

except:
    avl_0 = 0

try:
    couch1 = couchdb.Server('http://admin:admin@192.168.37.5:5984/')
    if "news" in couch1:
        db1 = couch1['news']
    else:
        db1 = couch1.create('news')

    avl_1 = 1
except:
    avl_1 = 0

try:
    couch2 = couchdb.Server('http://admin:admin@192.168.37.6:5984/')
    if "news" in couch2:
        db2 = couch2['news']
    else:
        db2 = couch2.create('news')

    avl_2 = 1
except:
    avl_2 = 0

couch_dns = couchdb.Server('http://admin:admin@192.168.37.4:5984/')

if "dns" in couch_dns:
    db_dns = couch_dns['dns']
else:
    db_dns = couch_dns.create('dns')

rond = 0
for root, dirs, files in os.walk('news/', topdown=False):
    for name in files:
        print(os.path.join(root, name))
        one_file = open(os.path.join(root, name), 'r')
        array_news = json.loads(one_file.read(), "utf8")
        for news in array_news:
            _id = news['id']
            del news['id']
            if _id not in db_dns:
                flag = 0
                if avl_0 == 0:
                    rond = (rond + 1) % 3
                elif rond == 0 and avl_0 == 1 and flag == 0:
                    db[_id] = news
                    db_dns[_id] = {"ip": "192.168.37.4", "backup": "192.168.37.5"}
                    rond = (rond + 1) % 3
                    flag = 1
                elif avl_1 == 0:
                    rond = (rond + 1) % 3
                elif rond == 1 and avl_1 == 1 and flag == 0:
                    db1[_id] = news
                    db_dns[_id] = {"ip": "192.168.37.5", "backup": "192.168.37.6"}
                    rond = (rond + 1) % 3
                    flag = 1
                elif avl_2 == 0:
                    rond = (rond + 1) % 3

                elif rond == 2 and avl_2 == 1 and flag == 0:
                    db2[_id] = news
                    db_dns[_id] = {"ip": "192.168.37.6", "backup": "192.168.37.4"}
                    rond = (rond + 1) % 3
                    flag = 1

            else:
                is_update_exist = False
                doc_ip = db_dns[_id]
                ip = doc_ip['ip']
                ip_backup = doc_ip['backup']
                if ip == "192.168.37.4" and avl_0 == 1:
                    news_inDb = db[_id]
                    for key in news.keys():
                        if news[key] != news_inDb.get(key):
                            news_inDb[key] = news[key]
                            is_update_exist = True
                            # print news

                    if is_update_exist:
                        db[news_inDb.id] = news_inDb

                if ip == "192.168.37.5" and avl_1 == 1:
                    news_inDb = db1[_id]
                    for key in news.keys():
                        if news[key] != news_inDb.get(key):
                            news_inDb[key] = news[key]
                            is_update_exist = True
                            print news

                    if is_update_exist:
                        db1[news_inDb.id] = news_inDb

                if ip == "192.168.37.6" and avl_2 == 1:
                    news_inDb = db2[_id]
                    for key in news.keys():
                        if news[key] != news_inDb.get(key):
                            news_inDb[key] = news[key]
                            is_update_exist = True
                            print news

                    if is_update_exist:
                        db2[news_inDb.id] = news_inDb
