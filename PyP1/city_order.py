from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import numpy as np
import re
import time
from sqlalchemy import create_engine
import pandas as pd
import json

driver = webdriver.Chrome(r"C:\Users\Felicity\Downloads\chromedriver_win32\chromedriver.exe")
driver.get("http://tianqi.2345.com/wea_history/54511.htm")

def isElementExist(element):
    flag = True
    try:
        content = driver.find_element_by_xpath(element)
        return content
    except:
        flag = False
        return flag
    
def clickprovince(p):
    driver.find_element_by_xpath('// *[ @ id = "switchHisCity"]').click()
    province = isElementExist('//*[@id="selectProv"]/option[' + str(p) + ']')
    return province


headers = ['province_cn', 'parent_cn', 'CN']
rows = [ ]
data = pd.DataFrame()
p = 1

while True:
    driver.get("http://tianqi.2345.com/wea_history/54511.htm")
    province = clickprovince(p)
    if province is False:
        break
    province.click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    p1 = r'[\u4e00-\u9fff]+'
    
    pro_list = soup.find_all(id='selectProv')#//*[@id="selectProv"]/option[1]
    for pro in pro_list:
        proall = pro.getText()   
    pro_list = re.findall(p1, proall)
    province = pro_list[p-1]
    
    parent_list = soup.find_all(id='chengs_ls')
    for pr in parent_list:
        parentall = pr.getText()
    parent_list = re.findall(p1, parentall)
    r = 1
    
    while True:
        parent = isElementExist('//*[@id="chengs_ls"]/option['+str(r)+']')

        if parent is False:
            break
        parent.click()
        parent = parent_list[r-1]
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        city_list = soup.find_all(id='cityqx_ls')
        for ct in city_list:
            cityall = ct.getText()
        city_list = re.findall(p1, cityall)

        r += 1

        df = pd.DataFrame(city_list, columns=['CN'])
        df['province_cn'] = province
        df['province_no'] = p
        df['parent_cn'] = parent
        df['parent_no'] = r
        df = df[['province_cn', 'province_no', 'parent_cn', 'parent_no','CN']]

        data = data.append(df)
        print(province, parent, len(city_list))

    p += 1
