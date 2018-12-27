import os
import glob
import json
from datetime import date
from datetime import timedelta
import operator
import json
import time
import random
import sys
from datetime import date


def search_flight(future_days=2,trip_days=7,year=2019,month=1,startday=1):
    lines = open('cities.txt').read().split("\n")
    f = open('parm.csv','w')
    result=[]
    for dest in lines:
        fromport='HKG'
        print(dest)
        if(len(dest)>0):
            for i in range(future_days):
                from_date = date(year,month,startday) + timedelta(days=i)
                to_date = from_date + timedelta(days=trip_days)
                from_date_str = from_date.strftime("%Y-%m-%d")
                to_date_str = to_date.strftime("%Y-%m-%d")
                outstr = fromport+','+dest+','+from_date_str+','+to_date_str
                f.write(outstr+'\n')
                result.append(outstr)
    return result

if ( len(sys.argv) >= 3 and sys.argv[1] == 'genall'):
        future=int(sys.argv[2])
        today = date.today() + timedelta(days=1)
        datalist=search_flight(future,7,today.year,today.month,today.day)

else:
    print("python gen_parm.py gen 30\n")
