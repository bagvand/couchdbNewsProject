#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys
import couchdb





couch = couchdb.Server()
couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')

#db = couch.create('addressbook')
#doc_id, doc_rev = db.save({'first_name': 'mehrdad', 'last_name': 'maherdad', 'phone' : 'hichi'})

db=couch['addressbook']

#doc = {'name': 'mehrdad2'}
#db.save(doc)


for id in db:
    print id




#file=open('my file','w')
#file.write('1,2,3,4,5')

file=open('ipna_4.txt','r')

print(file.read())

yourpath='e:/akhbar/'
for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
        print(os.path.join(root, name))
        file=open(os.path.join(root, name),'r')
        #print(file.read())
        x=file.read()
        doc = {'first_name': x}
        db.save(doc)
        
        
        
        
        
        
    for name in dirs:
        print(os.path.join(root, name))
        

#couchdbb=couchdb
#couchdbi=couchdbb.client.Server('http://admin:admin@127.0.0.1:5984')


#db=couchdbi.create['testt']
#db=couchdbi['testt']
#print("the data base name is "+db.name)

#doc_id ,doc_rev=db.save({'type':'person','name':'ali'})
#doc=db[doc_id]
#doc2={'name':'arash/ali22','type':'person'}
#db.save(doc2)

#print("_________________")
#print(doc)
#print("_________________")

#print(doc['type'])
#print(doc['name'])
#del db[doc.id]
#print(doc.id in db)

#print("tasks is")
#print(couchdbi.tasks())

#print("couchdb version")
#print(couchdbi.version())

#print(db.commit())

#print("add a doc with client uuid generator")
#doc_id3=uuid4().hex
#db[doc_id3]={'type':'person','name':'farnaz'}

#dos=dict(type='person',name='arash')
#db['arash22']=dos
#dos2=db['arash']
#dos2['age']=22
#db['arash']=dos2
#dos=db['arash']
#db.delete(dos)

#db.delete_attachment('arash','customerchurn.png')

#import image
#img=image.open('C:\Users\Programmer\Pictures\FootBall\0ef52a30-dc1c-11e3-8dcb-21ab1f7130ff_portugal_slogan.jpg')
#img.show()

#couchdbi.add_user('arashi','123')
#to=couchdbi.login('arash','123')
#print("User Token       "+to)
#print(couchdbi.verify_token(to))
#couchdbi.logout(to)
#print(couchdbi.verify_token(to))

#doc={'foo':'bar'}
#db.save(doc)
#couchdbi.login('arash','123')
#print(couchdbi.stats())
#for id in db:
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
#}'''
#    for row in db.query(map_fun,map_reduce):
#        print(row['key'])#row.key
#        print(row['value'])#row.value
        #break