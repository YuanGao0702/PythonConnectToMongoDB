# encoding=utf8
import selenium as se
from selenium.webdriver.common.by import By
import pymongo
from pprint import pprint
import sys
import time

CITY = "San Jose"



def weather(city):
    options = se.webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = se.webdriver.Chrome(chrome_options=options)
    url = 'https://www.google.com/search?hl=en&authuser=0&ei=M5YkXM_tOYzBjwTu47jABA&q='+city+'weather&oq=zhuozhou+weather&gs_l=psy-ab.3..35i39.1104929.1106580..1106843...0.0..0.97.684.9......0....1..gws-wiz.......0i71j0i7i30j0i7i5i10i30j0i13j0i13i30j0i8i13i30j35i304i39.kcZOPDwMDfs'
    driver.get(url)
    city = driver.find_element(By.XPATH,'//div[@class="vk_gy vk_h"][@id="wob_loc"]')
    #time = driver.find_element(By.XPATH,'//div[@class="vk_gy vk_sh"][@id="wob_dts"]')
    weather = driver.find_element(By.XPATH,'//img[@style="margin:1px 4px 0;height:48px;width:48px"]')
    tempMax = driver.find_element(By.XPATH,'//div[@class="vk_gy"]/span[@class="wob_t"]')
    tempMin = driver.find_element(By.XPATH,'//div[@class="vk_lgy"]/span[@class="wob_t"]')
    degree_sign= u'°'
    strOutput = city.text+'\n'+weather.get_attribute('alt')+'\n'+"Tempature: "+str(FtoC(tempMax.text))+degree_sign+' -- '+str(FtoC(tempMin.text))+degree_sign+'\n'
    aveTemp = (FtoC(tempMax.text)-FtoC(tempMin.text))/2+FtoC(tempMin.text)
    if aveTemp<=10:
    	strOutput = strOutput+"温度低，多穿点儿哈"
    print(strOutput)
    return strOutput

def FtoC(F):
    C = int((int(F)-32)*5/9+0.5)
    return C

def main():
    mongoConnectString = "mongodb://gaoyuan0702:Gw295459784!@ds213229.mlab.com:13229/react_node_express"
    myclient = pymongo.MongoClient(mongoConnectString)

    db = myclient["react_node_express"]
    col = db["weather"]

    query = {"City":CITY}
    col.delete_one(query)
    newValue = {"City":CITY,"Weather":weather(CITY)}
    col.insert_one(newValue)

    for x in col.find():
        pprint(x)

while(True):
    main()
    time.sleep(1800)
