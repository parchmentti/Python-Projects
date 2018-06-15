import json
from urllib import request
import pandas as pd
from datetime import date, timedelta
import datetime
from sqlalchemy import create_engine
import sched
import time

host = 'http://openapi.mlogcn.com:10880/api/w/fc/area/'

# scheduling an event that func runs at 2:30 pm
schedule = sched.scheduler(time.time, time.sleep)

def exe_every_day():
    x = datetime.datetime.today()
    y = x.replace(day=x.day, hour=14, minute=30, second=0, microsecond=0)
    excution_duration = (y - x).seconds + 1
    schedule.enter(excution_duration, 0, func, ())
    schedule.run()
    print(datetime.datetime.today())

    return None

# get url data
def get_page(area, startday, endday):
    xz_url = host + str(area) + '/d/' + startday + '/' + endday + '.json?token' + str(appid)
    data = ''
    with request.urlopen(xz_url) as f:
        data = f.read()
        data = data.decode('utf-8')

    return data

# write cleaned data into database
def write_page(area, startday, endday):
    flag = True
    try:
        result = get_page(area, startday, endday)
        result = json.loads(result)

        data1 = pd.DataFrame(result['series'])
        data2 = pd.DataFrame([[startday, area]] * len(data1.index), columns=['actual_day', 'area_code'])
        df = (pd.concat([data2, data1], axis=1))
        engine = create_engine(db_info)
        df.to_sql('weather', engine, schema= schema, index=False, if_exists='append')
        return flag
    except:
        flag = False
        return flag

# iterate through all areas, and return areas which failed to get the data
def pred_weather_40(areas, duration = 40):
    startday = date.today().strftime('%Y%m%d')
    endday = (date.today() + timedelta(days=duration)).strftime('%Y%m%d')
    error = []
    for area in areas:
        flag = write_page(area, startday, endday)
        if flag is False:
            print(area)
            error.append(area)

    return error

# iterate function pred_weather_40 until no element inside the error list
def func():
    e = pred_weather_40(areas)
    print('first round over: len =', len(e), ' Time:',datetime.datetime.today())
    while len(e)>0:
        e = pred_weather_40(e)
        print(len(e), datetime.datetime.today())

    print('success')

# runs the scheduler forever
while True:
    exe_every_day()
