#!/bin/sh

HOMEDIR='/app/flycheap/jmeter'
cd $HOMEDIR

ls |grep flight|grep json|xargs rm -f
echo "gen parm.csv"
python gen_parm.py genall 90
N=`wc -l parm.csv|awk '{print $1}'`
/opt/apache-jmeter-5.0/bin/jmeter -n -t  /app/flycheap/jmeter/hkexpress.jmx -JLOOPCNT=$N -JDIR=$HOMEDIR
echo "test completed"
cat /opt/apache-jmeter-5.0/bin/jmeter.log
ls |grep flight|grep json|wc -l
echo "upload"
ls|grep flycheap|grep firebase|grep adminsdk|grep json|xargs rm -f
while [ ! -f key.zip ] ; do
  pwd
  echo "waiting key"
  echo $CODE
  sleep 5
done

unzip -o -P $CODE key.zip
python upload.py
