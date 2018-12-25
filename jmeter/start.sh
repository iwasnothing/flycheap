#!/bin/sh

HOMEDIR='/Users/kahingleung/Documents/selenium_chrome/jmeter'
cd $HOMEDIR
rm -f flight0*json
python gen_parm.py
/Users/kahingleung/Downloads/apache-jmeter-5.0/bin/jmeter -n -t hkexpress.jmx -JLOOPCNT=20 -JDIR=$HOMEDIR
python upload.py
