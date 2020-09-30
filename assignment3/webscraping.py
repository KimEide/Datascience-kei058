import pandas as pd
import requests
from bs4 import BeautifulSoup

def scraper(url, name):
    # Reading the webpage
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    # Finding all data with the correct class
    data = soup.find_all(attrs={'class':'course-block__title'})
    items = []
    names = []

    # Finding the coursename only, and adds it to a list, add name to a different list for the dataframe
    for i in data:
        tmp = str(i)
        text = tmp.split('<h4 class="course-block__title">')[1]
        text = text.split('</h4>')[0]
        items.append(text)
        names.append(name)

    return pd.DataFrame({'tech':items, 'language':name})

if __name__ == "__main__":
    # Creating two different dataframes
    py_df = scraper("https://www.datacamp.com/courses/tech:python", 'python')
    r_df = scraper("https://www.datacamp.com/courses/tech:r", 'r')

    # Merging the two dataframes
    df = pd.concat([py_df, r_df])

    #Fixing index after concat
    df.reset_index(inplace=True, drop=True)
