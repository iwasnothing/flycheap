import os
import glob
import json
from datetime import date
from datetime import timedelta
import operator
import json
import time
import random

def search_flight(future_days=2,trip_days=7,year=2019,month=1,startday=1):
    lines = open('../cities.txt').read().split("\n")
    f = open('parm.csv','w')
    for dest in lines:
        fromport='HKG'
        print(dest)
        if(len(dest)>0):
            for i in range(future_days):
                from_date = date(year,month,startday) + timedelta(days=i)
                to_date = from_date + timedelta(days=trip_days)
                from_date_str = from_date.strftime("%Y-%m-%d")
                to_date_str = to_date.strftime("%Y-%m-%d")
                f.write(fromport+','+dest+','+from_date_str+','+to_date_str+'\n')




search_flight(2,7,2019,1,1)
