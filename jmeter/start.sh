#!/bin/sh

python gen_parm.py
/Users/kahingleung/Downloads/apache-jmeter-5.0/bin/jmeter -n -t hkexpress.jmx -JLOOPCNT=20
python upload.py
