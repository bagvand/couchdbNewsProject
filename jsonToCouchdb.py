#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import couchdb
import json

couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')

db = couch['news']

for root, dirs, files in os.walk('news/', topdown=False):
    for name in files:
        print(os.path.join(root, name))
        one_file = open(os.path.join(root, name), 'r')
        array_news = json.loads(one_file.read(), "utf8")
        for news in array_news:
            _id = news['id']
            del news['id']
            if _id not in db:
                db[_id] = news
            else:
                is_update_exist = False
                news_inDb = db[_id]
                for key in news.keys():
                    if news[key] != news_inDb.get(key):
                        news_inDb[key] = news[key]
                        is_update_exist = True
                        print news

                if is_update_exist:
                    db[news_inDb.id] = news_inDb


                # couchdbb=couchdb
                # couchdbi=couchdbb.client.Server('http://admin:admin@127.0.0.1:5984')

                # db=couchdbi.create['testt']
                # db=couchdbi['testt']
                # print("the data base name is "+db.name)

                # doc_id ,doc_rev=db.save({'type':'person','name':'ali'})
                # doc=db[doc_id]
                # doc2={'name':'arash/ali22','type':'person'}
                # db.save(doc2)

                # print("_________________")
                # print(doc)
                # print("_________________")

                # print(doc['type'])
                # print(doc['name'])
                # del db[doc.id]
                # print(doc.id in db)

                # print("tasks is")
                # print(couchdbi.tasks())

                # print("couchdb version")
                # print(couchdbi.version())

                # print(db.commit())

                # print("add a doc with client uuid generator")
                # doc_id3=uuid4().hex
                # db[doc_id3]={'type':'person','name':'farnaz'}

                # dos=dict(type='person',name='arash')
                # db['arash22']=dos
                # dos2=db['arash']
                # dos2['age']=22
                # db['arash']=dos2
                # dos=db['arash']
                # db.delete(dos)

                # db.delete_attachment('arash','customerchurn.png')

                # import image
                # img=image.open('C:\Users\Programmer\Pictures\FootBall\0ef52a30-dc1c-11e3-8dcb-21ab1f7130ff_portugal_slogan.jpg')
                # img.show()

                # couchdbi.add_user('arashi','123')
                # to=couchdbi.login('arash','123')
                # print("User Token       "+to)
                # print(couchdbi.verify_token(to))
                # couchdbi.logout(to)
                # print(couchdbi.verify_token(to))

                # doc={'foo':'bar'}
                # db.save(doc)
                # couchdbi.login('arash','123')
                # print(couchdbi.stats())
                # for id in db:
                #   tdoc=db[id]
                #  if (tdoc['name']=='arash/ali22'):
                #        tdoc['name']='arash/ali223'
                #        tdoc['edu']='arshad'
                #        db[tdoc.id]=tdoc
                #        del db[tdoc.id]
                #    print(tdoc['name']+"   "+tdoc['type'])

                # map_fun = '''function(doc){
                #        if(doc.type=='person')
                #            emit(doc.type,doc.name);
                #    }'''
                #    map_reduce='''function(key,values,rereduce){
                #   return values.length;
                # }'''
                #    for row in db.query(map_fun,map_reduce):
                #        print(row['key'])#row.key
                #        print(row['value'])#row.value
                # break
