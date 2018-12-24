import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import date
from datetime import timedelta
import operator
import json
import time

def parse_flight(strlist):
    l = len(strlist)
    response = {"time": strlist[0], "found": 0}
    for i in range(l):
        if(strlist[i] == 'duration' and i+2 < l):
            response['flightnum']= strlist[i+2]

        try:
            trynum = int(strlist[i].replace(',',''))
            response['price'] = trynum
            response['found'] = 1
        except ValueError:
            print("not a number")


    return response





chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
#chrome_options.add_argument('--proxy-server={}'.format(proxy))
chrome_driver = os.getcwd() + "/chromedriver"
print(chrome_driver)
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
#driver = webdriver.Firefox()
driver.implicitly_wait(20)

def write_output(filename,list):
    f = open(filename, "w")
    for line in list:
        json.dump(line, f)
        f.write("\n")
    f.close()

def search_flight(orig='HKG',dest='KIX',future_days=2,trip_days=5,year=2019,month=1,startday=1):
    price_list = []
    #orig = "HKG"
    #dest = "KIX"

    for i in range(future_days):
        time.sleep( 1 )
        from_date = date(year,month,startday) + timedelta(days=i)
        to_date = from_date + timedelta(days=trip_days)
        from_date_str = from_date.strftime("%d/%m/%Y")
        to_date_str = to_date.strftime("%d/%m/%Y")
        search_url = "https://booking.hkexpress.com/en-US/select/?SearchType=RETURN&OriginStation=" + orig + "&DestinationStation=" + dest + "&DepartureDate=" + from_date_str + "&ReturnDate=" + to_date_str + "&Adults=1&LowFareFinderSelected=false"
        #driver.get("https://booking.hkexpress.com/en-US/select/?SearchType=RETURN&OriginStation=HKG&DestinationStation=KIX&DepartureDate=02/01/2019&ReturnDate=05/01/2019&Adults=1&LowFareFinderSelected=false")
        print(search_url)
        driver.get(search_url)
        #print(driver.page_source)
        try:
            #price = driver.find_element_by_xpath("//main[@id='maincontent']/div[2]/div/div/flight-schedule-container/schedule-tabs/div/ibe-tab-panel/div[2]/div/flight/div/div[4]/button/span[2]")
            #price = driver.find_element_by_xpath("//main[@id='maincontent']")
            #print(price.text)
            #wait = WebDriverWait(driver, 20)
            #elem = wait.until(EC.element_to_be_clickable((By.cssSelector,'.colPrices')))
            #prices = driver.find_elements_by_css_selector(".colPrices")
            rows = driver.find_elements_by_css_selector(".rowFlight")
            prices = driver.find_elements_by_css_selector(".price")
            i = 0
            for row in rows:
                token = row.text.split()
                print("prices")
                print(token)

                response = parse_flight(token)
                response['date'] = from_date_str

                print(response)
                if(response["found"] == 1):
                    price_list.append(response)
                else:
                    driver.get_screenshot_as_file('empty.png')

                i = i + 1

        except NoSuchElementException:
            print("not found")
            driver.get_screenshot_as_file('error.png')

    print("-----result-----")
    price_list = sorted(price_list,key=lambda k: k['price'])
    print(price_list[:3])
    write_output("flight_"+orig+dest+".json", price_list)

lines = open('cities.txt').read().split("\n")
for dest in lines:
    print(dest)
    if(len(dest)>0):
        search_flight('HKG',dest,30,7,2019,1,1)
