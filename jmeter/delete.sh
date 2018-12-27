#!/bin/sh
HOMEDIR='/home/iwasnothing/flycheap/jmeter'
cd $HOMEDIR
kubectl get pods --output=wide
touch out.log
PODLIST=`kubectl get pods --output=wide|grep flycheap|grep Completed|awk '{print $1}'`
for pod in $PODLIST ; do
    kubectl logs $pod >> out.log
gcloud container clusters delete flycheap01 --zone=us-central1-a --quiet
