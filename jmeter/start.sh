#!/bin/sh

HOMEDIR='/app/flycheap/jmeter'
cd $HOMEDIR
zip -P 94077079 key.zip flycheap*json

gcloud container clusters create flycheap01 --zone=us-central1-a --num-nodes=1 --preemptible
gcloud container clusters get-credentials --zone=us-central1-a flycheap01
n=0
while [ n -ne 3] ; do
  n=`kubectl get pods --output=wide|grep -c Running`
done
IPLIST=`kubectl get pods --output=wide|grep flycheap|awk '{print $6}'`
PODLIST=`kubectl get pods --output=wide|grep flycheap|awk '{print $1}'`
kubectl cp parm.csv $PODLIST:/app/flycheap/jmeter/parm.csv
kubectl cp key.zip $PODLIST:/app/flycheap/jmeter/key.zip
kubectl create -f onejob.yml
