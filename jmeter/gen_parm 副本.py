import os
import glob
import json
from datetime import date
from datetime import timedelta
import operator
import json
import time
import random
import sys
from datetime import date
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def search_flight(future_days=2,trip_days=7,year=2019,month=1,startday=1):
    lines = open('cities.txt').read().split("\n")
    f = open('parm.csv','w')
    result=[]
    for dest in lines:
        fromport='HKG'
        print(dest)
        if(len(dest)>0):
            for i in range(future_days):
                from_date = date(year,month,startday) + timedelta(days=i)
                to_date = from_date + timedelta(days=trip_days)
                from_date_str = from_date.strftime("%Y-%m-%d")
                to_date_str = to_date.strftime("%Y-%m-%d")
                outstr = fromport+','+dest+','+from_date_str+','+to_date_str
                f.write(outstr+'\n')
                result.append(outstr)
    return result

found=0
for key in glob.glob('flycheap-*.json'):
    cred = credentials.Certificate(key)
    firebase_admin.initialize_app(cred)
    found = 1
if(found == 0):
    firebase_admin.initialize_app()
db = firestore.client()

transaction = db.transaction()
city_ref = db.collection('config').document('counter')

@firestore.transactional
def update_in_transaction(transaction, city_ref):
    snapshot = city_ref.get(transaction=transaction)
    current = snapshot.get('current')
    total = snapshot.get('total')
    new_value = (current + 1)%total

    transaction.update(city_ref, {
            'current': new_value
        })
    return current



def init_counter(total):
    data = {
        'current': 0,
        'total': total,
    }
    city_ref.set(data)


if (len(sys.argv) >= 3 and sys.argv[1] == 'init'):
        total=int(sys.argv[2])
        init_counter(total)
elif ( len(sys.argv) >= 3 and sys.argv[1] == 'gen'):
        future=int(sys.argv[2])
        today = date.today() + timedelta(days=1)
        datalist=search_flight(future,7,today.year,today.month,today.day)
        i = update_in_transaction(transaction, city_ref)
        doc = city_ref.get().to_dict()
        totalnode = doc['total']
        l=len(datalist)
        batch_size = int(l/totalnode)+1
        startidx = i*batch_size
        if(i == totalnode -1):
            endidx = l
        else:
            endidx = (i+1)*batch_size
        outf = open('nodeparm.csv','w')
        print('idx value: {} {} {} {} {}'.format(i,l,batch_size,startidx,endidx))
        for row in datalist[startidx:endidx]:
            outf.write(row+'\n')
elif ( len(sys.argv) >= 3 and sys.argv[1] == 'genall'):
        future=int(sys.argv[2])
        today = date.today() + timedelta(days=1)
        datalist=search_flight(future,7,today.year,today.month,today.day)
        #doc = city_ref.get().to_dict()
        #totalnode = doc['total']
        totalnode=3
        l=len(datalist)
        batch_size = int(l/totalnode)+1
        for i in range(totalnode):
            startidx = i*batch_size
            if(i == totalnode -1):
                endidx = l
            else:
                endidx = (i+1)*batch_size
            outf = open('nodeparm_{}.csv'.format(i),'w')
            print('idx value: {} {} {} {} {}'.format(i,l,batch_size,startidx,endidx))
            for row in datalist[startidx:endidx]:
                outf.write(row+'\n')
else:
    print("python gen_parm.py init 3\n")
    print("python gen_parm.py gen 30\n")
