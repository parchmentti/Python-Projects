
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import numpy as np
from calendar import monthrange

# Header
name = ['Date', 'Mean', 'Max', 'Min', 'rain', 'wind', 'visibility']

#return recent year's weather details with max year specified
def weather_c(year_max, mth_max, day_max):
    data2 = []
    for year in range(year_max - 2, year_max+1):
        for mth in range(1,13):
            day_threshold = monthrange(year, mth)[1] + 1

            for day in range(1, day_threshold):

                print(year, mth, day)

                if year == year_max and mth == mth_max and day ==day_max:
                    return data2

                theDate = str(year)+"/" + str(mth) + "/" + str(day)
                url = "http://www.wunderground.com/history/airport/ZBAA/" + theDate + "/DailyHistory.html"
                response = urllib.request.urlopen(url)
                r = BeautifulSoup(response, "html.parser")

                m = r.find_all(id="historyTable")

                child = m[0].find_all('td', 'indent')
                data2.append(theDate)
                for i in range(0, len(child)-1):
                    col = child[i].get_text()
                    if col in ('Mean Temperature', 'Max Temperature', 'Min Temperature', 'Precipitation', 'Wind Speed', 'Visibility'):
                        data2.append(child[i].parent.find_all('span','wx-value')[0].get_text())

data = weather_c(2018,5,31)
shape = (int(len(data)/7),7)
weather_bj = pd.DataFrame(np.array(data).reshape(shape), columns = name)

