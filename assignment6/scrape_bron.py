import requests
from bs4 import BeautifulSoup
import calendar
import matplotlib.pyplot as plt
import datetime
import time

def find_days_in_month(year, month):
    return calendar.monthrange(year, month)[1]

def retrive_count(year, month, county_list):
    url = 'https://w2.brreg.no/kunngjoring/kombisok.jsp?datoFra=01.{}.{}&datoTil={}.{}.{}&id_region=0&id_niva1=51&id_niva2=56&id_bransje1=0'.format('%02d' % month, year, find_days_in_month(year, month),'%02d' % month, year)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    count = 0
    city = 'a'
    count_list = list(range(len(county_list)))
    for tr in soup.findAll('tr'):
        if tr.find('strong'):
            if city in county_list:
                # print(count, city)
                count_list[county_list.index(city)] = count
            city = tr.find('strong').text.strip()
            count = 0
        if tr.find('a', href=True):
            if tr.find('a').text.strip() == 'Konkursåpning' or tr.find('a').text.strip() == 'Konkursåpning i hjemlandet':
                count += 1

    if city in county_list:
        count_list.append(count)


    for i in range(len(count_list), len(county_list)):
        count_list.append(0)


    return count_list

def find_number():
    counties = ['Oslo', 'Rogaland', 'Møre og Romsdal', 'Nordland', 'Viken', 'Innlandet', 'Vestfold og Telemark', 'Agder', 'Vestland', 'Trøndelag', 'Troms og Finnmark', 'Utenlands', 'Svalbard']
    month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    countlist = []
    count = list(range(len(counties)))
    max_count = 0
    monthlist = []
    for year in range(2019, 2021):
        count.clear()
        countlist.clear()
        monthlist.clear()
        count = list(range(len(counties)))
        countlist = [[] for i in range(len(counties))]
        for month in range(1, 13):
            if datetime.date.today().year <= year and datetime.date.today().month < month:
                break
            monthly_count = retrive_count(year, month, counties)
            monthlist.append(month)
            for county in counties:
                count[counties.index(county)] += monthly_count[counties.index(county)]
                countlist[counties.index(county)].append(count[counties.index(county)])
                if max_count < count[counties.index(county)]:
                    max_count = count[counties.index(county)]
            countlist.append(count)
        for county in counties:
            plt.figure(counties.index(county))
            plt.plot(monthlist, countlist[counties.index(county)], label=year)
    

    for county in counties:
        plt.figure(counties.index(county))
        plt.ylim(0, max_count + 100)
        plt.xticks(list(range(1,13)), month_name)
        plt.legend(loc="upper left")
        plt.title(county)
        plt.savefig(county)
        plt.close()

if __name__ == "__main__":
    start = time.time()
    find_number()
    end = time.time()

    print('runtime is {}'.format(end-start))
