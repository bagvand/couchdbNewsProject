#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import couchdb
import json


class ParentServer:
    def __init__(self, ip, port=5984, username='admin', password='admin'):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.couch_server = None
        self.set_couch_server()

    def set_couch_server(self):
        try:
            self.couch_server = couchdb.Server(self.get_server_address())
            return True
        except:
            self.couch_server = None

        return False

    def get_server_address(self):
        return "http://" + self.username + ":" + self.password \
               + "@" + self.ip + ":" + self.port + "/"


class DnsServer(ParentServer):
    def __init__(self, ip, port=5984, username='admin', password='admin'):
        super.__init__(ip, port, username, password)

    def get_dns_database(self):
        dns_db = None
        try:
            if (self.couch_server is not None) or self.set_couch_server():
                if "dns" in self.couch_server:
                    dns_db = self.couch_server['dns']
                else:
                    dns_db = self.couch_server.create('dns')
        except:
            pass

        return dns_db


class Server(ParentServer):
    def __init__(self, ip, port=5984, username='admin', password='admin'):
        super.__init__(ip, port, username, password)

    def get_news_database(self):
        news_db = None
        try:
            if (self.couch_server is not None) or self.set_couch_server():
                if "news" in self.couch_server:
                    news_db = self.couch_server['news']
                else:
                    news_db = self.couch_server.create('news')
        except:
            pass

        return news_db

    def is_available(self):
        if self.get_news_database() is None:
            return False
        return True

    def is_this_server(self, ip):
        if self.ip == ip:
            return True
        return False


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
                    server_dns.get_dns_database()[_id] = {"ip": "192.168.37.4", "backup": "192.168.37.5"}
                    rond = (rond + 1) % 3
                    flag = 1
                elif not server1.is_available():
                    rond = (rond + 1) % 3
                elif rond == 1 and server1.is_available() and flag == 0:
                    server1.get_news_database()[_id] = news
                    server_dns.get_dns_database()[_id] = {"ip": "192.168.37.5", "backup": "192.168.37.6"}
                    rond = (rond + 1) % 3
                    flag = 1
                elif not server2.is_available():
                    rond = (rond + 1) % 3

                elif rond == 2 and server2.is_available() and flag == 0:
                    server2.get_news_database()[_id] = news
                    server_dns.get_dns_database()[_id] = {"ip": "192.168.37.6", "backup": "192.168.37.4"}
                    rond = (rond + 1) % 3
                    flag = 1

            else:
                is_update_exist = False
                doc_ip = server_dns.get_dns_database()[_id]
                ip = doc_ip['ip']
                ip_backup = doc_ip['backup']
                news_inDb = None

                db = None
                if server0.is_this_server(ip) and server0.is_available():
                    db = server0.get_news_database()
                elif server1.is_this_server(ip) and server1.is_available():
                    db = server1.get_news_database()
                elif server2.is_this_server(ip) and server2.is_available():
                    db = server2.get_news_database()

                news_inDb = db[_id]
                for key in news.keys():
                    if news[key] != news_inDb.get(key):
                        news_inDb[key] = news[key]
                        is_update_exist = True

                if is_update_exist:
                    db[news_inDb.id] = news_inDb
