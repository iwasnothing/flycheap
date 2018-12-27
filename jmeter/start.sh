#!/bin/sh
HOMEDIR='/home/iwasnothing/flycheap/jmeter'
cd $HOMEDIR
#zip -P 94077079 key.zip flycheap*json
gcloud container clusters create flycheap01 --zone=us-central1-a --num-nodes=1 --preemptible
gcloud container clusters get-credentials --zone=us-central1-a flycheap01
kubectl create -f onejob.yml
n=0
while [ $n -ne 1 ] ; do
        echo "gettig pod"
        kubectl get pods --output=wide
        n=`kubectl get pods --output=wide|grep -c Running`
        sleep 3
done
IPLIST=`kubectl get pods --output=wide|grep flycheap|awk '{print $6}'`
PODLIST=`kubectl get pods --output=wide|grep flycheap|awk '{print $1}'`
#kubectl cp parm.csv $PODLIST:/app/flycheap/jmeter/parm.csv
kubectl cp key.zip $PODLIST:/app/flycheap/jmeter/key.zip
