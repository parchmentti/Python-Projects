from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome(r"C:\Users\Felicity\Downloads\chromedriver_win32\chromedriver.exe")
driver.get("http://api.map.baidu.com/lbsapi/getpoint/index.html")
store = pd.read_csv(path, index_col=0)
store_list = store['store_desc']
address = []
coor_x = []
coor_y = []

# check the existence of an element, return False if not
def isElementExist():
    flag = True
    try:
        content = soup.find_all('p')[0].getText()
        return content
    except:
        flag = False
        return flag

def get_geo(store_list):
    for k in store_list:
        driver.get("http://api.map.baidu.com/lbsapi/getpoint/index.html")
        text_area = driver.find_element_by_xpath('//*[@id="localvalue"]')
        text_area.send_keys(k)
        text_area.send_keys(Keys.RETURN)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content = isElementExist()
        # Assign 'NA' value to stores not found
        if content is False:
            address.append('NA')
            coor_x.append('NA')
            coor_y.append('NA')

        # organise the result into desired format
        else:
            content = content.split("      ")
            result = [item for item in content if item.startswith('地址')][0]
            address.append(result.split("：")[1])
            coor = [item for item in content if item.startswith('坐标')][0]
            coor = coor.split("：")[1]
            coor_x.append(coor.split(",")[0])
            coor_y.append(coor.split(",")[1])


    store_list = pd.DataFrame(store_list)
    address = pd.DataFrame(address)
    coor_x = pd.DataFrame(coor_x)
    coor_y = pd.DataFrame(coor_y)
    test = pd.concat([store_list, address, coor_x, coor_y], axis = 1)
    test.columns = ['store_desc', 'address', 'coor_x', 'coor_y']

    return test


test = get_geo(store_list)
data = pd.concat([store, test], axis = 1)
data.to_csv('C:\\Users\\Felicity\\Desktop\\store.csv', header=True, index=False, encoding = 'utf_8_sig')