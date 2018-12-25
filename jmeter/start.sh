#!/bin/sh

python gen_parm.py
rm -f flight*json
JMDIR="/Users/kahingleung/Downloads/apache-jmeter-5.0/bin"
$JMDIR/jmeter -n -t hkexpress.jmx -JLOOPCNT=20
python upload.py
