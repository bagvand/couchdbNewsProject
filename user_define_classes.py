import couchdb


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

    def is_this_server(self, address):
        if self.get_server_address() == address:
            return True
        return False


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