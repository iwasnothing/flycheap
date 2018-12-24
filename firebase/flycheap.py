import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json


def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(10).get()
    deleted = 0

    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

key="./flycheap-285b7-firebase-adminsdk-b1t26-a78a060baf.json"
cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)
db = firestore.client()

lines = open('../cities.txt').read().split("\n")
for dest in lines:
    print(dest)
    if(len(dest)>0):
        datafile = open('../flight_HKG'+dest+'.json').read().split("\n")
        coll_ref = db.collection('cities').document(dest).collection('flight')
        batch_size = 5
        delete_collection(coll_ref, batch_size)
        for flight in datafile:
            print(flight)
            if(len(flight)>0):
                doc = json.loads(flight)
                db.collection('cities').document(dest).collection('flight').add(doc)
