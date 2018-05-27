from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
import numpy
import pandas
import re
from sqlalchemy import create_engine

#in case you want to write the data into SQL
engine=create_engine('postgresql+psycopg2://username:password@host:port/database')


#open with Chrome
driver = webdriver.Chrome(r"C:\Users\Felicity\Downloads\chromedriver_win32\chromedriver.exe")
driver.get("http://tianqi.2345.com/wea_history/54511.htm")
time.sleep(1)

# check the existence of an element, return False if not

def isElementExist(element):
    flag = True
    try:
        content = driver.find_element_by_xpath(element)
        return content
    except:
        flag = False
        return flag

#
# 创建一个带表头的csv文件
headers = ['city', 'date', 'high', 'low', 'weather', 'cloud', 'air']
f = open('C:\\Users\\Felicity\\Desktop\\test.csv', 'w', encoding = 'utf-8')
writer = csv.writer(f)
writer.writerow(headers)
f.close()

rows = [ ]
p = 1

# choose province/region
def clickprovince(p):
    driver.find_element_by_xpath('// *[ @ id = "switchHisCity"]').click()
    province = isElementExist('//*[@id="selectProv"]/option[' + str(p) + ']')
    return province

def weather_crawling(p):
    while True:
        # get data from server
        driver.get("http://tianqi.2345.com/wea_history/54511.htm")
        # get xpath of 'province'
        province = clickprovince(p)
        # print(province)
        if province is False:
            break
        # choose 'province'
        province.click()
        # get the source code of current page
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # find city list
        cityall = soup.find_all(id='chengs_ls')
        # regular expression of Chinese characters
        p1 = r'[\u4e00-\u9fff]+'
        # get city list
        for ct in cityall:
            temp = ct.getText()
        c = 1
        #loop over city list
        while True:
            city = isElementExist('//*[@id="chengs_ls"]/option['+str(c)+']')

            if city is False:
                break
            city.click()
            # get the name of current city
            city = re.findall(p1, temp)[c-1]

            driver.find_element_by_xpath('//*[@id="buttonsdm_dz"]').click()

            # starting from 2016
            i = 6
            rows = [ ]
            #loop over 'year'
            while True:
                driver.find_element_by_id('chooseHisYear').click()
                year = isElementExist('//*[@id="chooseHisYear"]/ul/li['+str(i)+']')
                if year is False:
                    clickprovince(p).click()
                    break
                year.click()
                j= 1

                #loop over 'month'
                while j < 13:
                    driver.find_element_by_id('chooseHisMonth').click()
                    month = isElementExist('//*[@id="chooseHisMonth"]/ul/li['+str(j)+']')
                    month.click()
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    weather = soup.find_all('td')
                    #rows restore all specifics of the city
                    # 保存一个城市的所有天气信息
                    for t in weather:
                        rows.append([t.getText()])
                    j = j + 1

                i += 1

            c += 1
            # organise the weather information into data frame
            shape = (int(len(rows) / 6), 6)
            arr = numpy.array(rows).reshape(shape)
            data1 = pandas.DataFrame(numpy.array(rows).reshape(shape),
                                     columns=['date', 'high', 'low', 'weather', 'cloud', 'air'])
            data2 = pandas.DataFrame([city] * len(data1.index), columns=['city'])
            df = (pandas.concat([data2, data1], axis=1))
            #write into csv
            df.to_csv('C:\\Users\\Felicity\\Desktop\\test.csv', mode='a', header=False, index=False)
            #write into SQL
            df.to_sql('city_weather', engine, if_exists = 'append')

        p += 1



 weather_crawling(p)

