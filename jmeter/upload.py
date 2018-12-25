import os
import glob
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def parse_flight(flight):
    doc = {
        'from': flight['segments'][0]['departureStationCode'],
        'to': flight['segments'][0]['arrivalStationCode'],
        'date': flight['segments'][0]['departureDate'],
        'fightnum': flight['segments'][0]['flightNumber'],
        'price': flight['fares'][0]['amount']
    }
    if(doc['from'] == 'HKG'):
        doc['return'] = 0
        doc['dest'] = doc['to']
    else:
        doc['return'] = 1
        doc['dest'] = doc['from']
    print(doc)
    return doc


def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(10).get()
    deleted = 0

    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def upload_flight(flight):
    db = firestore.client()
    doc = parse_flight(flight)
    dest = doc['dest']
    print(dest)
    db.collection('cities').document(dest).collection('flight').add(doc)

key="./flycheap-285b7-firebase-adminsdk-q6d7x-699ad6ba77.json"
cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)
db = firestore.client()

lines = open('../cities.txt').read().split("\n")
for dest in lines:
    print(dest)
    if(len(dest)>0):
        coll_ref = db.collection('cities').document(dest).collection('flight')
        batch_size = 5
        delete_collection(coll_ref, batch_size)

for filename in glob.glob('flight*.json'):
  print(filename)
  str = open(filename).read()
  d = json.loads(str)
  to_flights = d['trips'][0]['flights']
  return_flights = d['trips'][1]['flights']
  for flight in to_flights:
      upload_flight(flight)
  for flight in return_flights:
      upload_flight(flight)
