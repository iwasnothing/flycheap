#!/bin/sh

HOMEDIR='/app/flycheap/jmeter'
cd $HOMEDIR
rm -f flight0*json
python gen_parm.py gen 30
#N=`wc -l nodeparm.csv|awk '{print $1}'`
#echo $N
#/opt/apache-jmeter-5.0/bin/jmeter -n -t hkexpress.jmx -JLOOPCNT=$N -JDIR=$HOMEDIR
/opt/apache-jmeter-5.0/bin/jmeter-server
