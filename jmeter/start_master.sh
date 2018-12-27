#!/bin/sh
#gcloud components install kubectl
sudo apt-get install kubectl

#gcloud builds submit --tag gcr.io/iwasnothing03/flycheap-slave .
gcloud container clusters create flycheap01 --zone=us-central1-a --num-nodes=4 --preemptible
gcloud container clusters get-credentials --zone=us-central1-a flycheap01
#kubectl run hello-world --replicas=5 --labels="run=load-balancer-example" --image=gcr.io/google-samples/node-hello:1.0  --port=8080
kubectl run flycheap-slave --replicas=3 --labels="role=slave" --image gcr.io/iwasnothing03/flycheap-slave --port 1099
#kubectl run flycheap-master --replicas=1 --labels="role=master" --image gcr.io/flycheap-285b7/flycheap-master --port 1099
n=0
while [ n -ne 3] ; do
  n=`kubectl get pods --output=wide|grep -c Running`
done
IPLIST=`kubectl get pods --output=wide|grep flycheap|awk '{print $6}'`
PODLIST=`kubectl get pods --output=wide|grep flycheap|awk '{print $1}'`


#kubectl exec -it flycheap-slave-56b885f7b8-d5bsp -- /bin/bash
#kubectl expose deployment jmeter-server --port 1099 --target-port 1099
#kubectl get service jmeter-server
for pod in $PODLIST ; do
kubectl cp ../jmeter/nodeparm_0.csv flycheap-slave-56b885f7b8-587km:/app/flycheap/jmeter/parm.csv
kubectl cp ../jmeter/nodeparm_1.csv flycheap-slave-56b885f7b8-9djsd:/app/flycheap/jmeter/parm.csv
kubectl cp ../jmeter/nodeparm_2.csv flycheap-slave-56b885f7b8-nqpr4:/app/flycheap/jmeter/parm.csv
kubectl create -f job.yml
kubectl cp flycheap-slave-56b885f7b8-9djsd:/app/flycheap/jmeter out02
# copy rmi key and firestore json to pod
#HOMEDIR='/app/flycheap/jmeter'

#N=`wc -l nodeparm.csv|awk '{print $1}'`
#echo $N
#/opt/apache-jmeter-5.0/bin/jmeter -n -t hkexpress.jmx -GLOOPCNT=$N -GDIR=$HOMEDIR
#/opt/apache-jmeter-5.0/bin/jmeter-server
gcloud container clusters delete flycheap01 --zone=us-central1-a --quiet
