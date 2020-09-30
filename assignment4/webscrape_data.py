import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    data = soup.findAll(attrs={'class':'table-primary'})
    date = []

    for tr in data:
        td = tr.findAll('td')
        tmp = str(td[0])
        tmp = tmp.split('<br/>')[1]
        tmp = tmp.split('</td>')[0]
        date.append(tmp)

    return pd.DataFrame({'Date':date})
    
if __name__ == "__main__":
    df = scrape('http://timeplan.uit.no/emne_timeplan.php?sem=20h&module%5B%5D=BED-2056-1&View=list')