from urllib.parse import quote
from urllib import request
import string
import pandas as pd
import json


baidu_web_key = 'Your_key'
poi_search_url = "http://api.map.baidu.com/place/v2/search"

store['location'] = store['coor_y'].apply(str) + ',' + store['coor_x'].apply(str)

store = store.rename(columns={'store_desc.1': 'target_desc'})

store = store[-store['address'].isnull()]

radius = 3000

#get poi according to 'type' and 'location'
def getpois(location, queries, num):
    poilist = pd.DataFrame(columns=['location', 'type', 'area', 'name', 'address'])
    for loc in location[num:]:
        engine = create_engine('postgresql://felicity_liao:analyst*%$830@da-db-1.czec8chdqeuo.rds.cn-north-1.amazonaws.com.cn:5432/postgres')
        for query in queries:
            i = 0
            print(loc, query)
            while True : #使用while循环不断分页获取数据
                print(i)

                result = getpoi_page(loc, query, i)
                result = json.loads(result)  
#                test = islisttExist(**result)

                if len(result['results']) == 0:
                    break

                result = pd.DataFrame(result['results'])
                data1 = result[['area', 'name', 'address']]
                #if data1 is False:
                #    break
                data2 = pd.DataFrame([[loc, query]] * len(data1.index), columns=['location', 'type'])
                df = (pd.concat([data2, data1], axis=1))
                poilist = pd.concat([poilist, df], ignore_index= True)
                df.to_sql('bd_pois', engine, schema='analyst', index=False,if_exists='append')
                #df.to_csv('C:\\Users\\Felicity\\Desktop\\bd_pois.csv', mode='a', header=False, index=False, encoding='utf_8_sig')
                i = i + 1
    return poilist

def getpoi_page(loc, query, page):
    req_url = poi_search_url + "?query=" + query +"&location=" + \
              quote(loc) + '&offset=25' + '&radius=' + str(radius) + '&page_size=20' + '&page_num=' + str(page) + '&output=json&ak=' + baidu_web_key
    r = quote(req_url,safe=string.printable) #quote的参数表示可以忽略的字符
                                            #string.printable表示ASCII码第33～126号可打印字符，
                                            # 其中第48～57号为0～9十个阿拉伯数字；65～90号为26个大写英文字母，
                                            # 97～122号为26个小写英文字母，其余的是一些标点符号、运算符号等
    data = ''
    with request.urlopen(r) as f:
        data = f.read()
        data = data.decode('utf-8')

    return data



cityname = "北京"
queries = ['美食','酒店',
'购物',
'生活服务',
'丽人',
'旅游景点',
'休闲娱乐',
'运动健身',
'教育培训',
'文化传媒',
'医疗',
'汽车服务',
'交通设施',
'金融',
'房地产',
'公司企业',
'政府机构',
'出入口',
'自然地物'
]
keywords_list = store['target_desc']
keywords_list = keywords_list.tolist()
location = store['location'].tolist()

pois = getpois(location, queries, 0)
pois = pd.DataFrame.drop_duplicates(pois)

pois.to_csv('C:\\Users\\Felicity\\Desktop\\pois.csv',header=True, index=False)

print('写入成功')


