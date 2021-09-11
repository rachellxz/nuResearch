import requests
from bs4 import BeautifulSoup
import pandas as pd

### MASTER CATALOG SCRAPER - NO NEED TO RUN AGAIN ###
def scrape_catalog():
    channels = []
    r = requests.get('https://www.newswise.com/channels/rss')
    s = BeautifulSoup(r.text,'html.parser')
    for i in s.find_all(class_ = 'channel-list'):
        try:
            genre = i.find('h3').text
            for j in i.find_all('a'):
                channel = j.text
                url = 'https://www.newswise.com' + j['href']
                channels.append({'genre': genre, 'channel': channel, 'url': url})
        except Exception:
            pass

    channels_df = pd.DataFrame(channels)
    channels_df.to_csv("catalog.csv")
    print("Channels catalog saved to 'catalog.csv'")

if __name__ == "__main__":
    scrape_catalog()
