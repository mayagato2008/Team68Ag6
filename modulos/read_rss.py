import pandas as pd
import requests
from bs4 import BeautifulSoup

def rss():
    url = "https://www.eltiempo.com/rss/justicia_conflicto-y-narcotrafico.xml"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, features ="xml")
    items = soup.findAll('item')
    news_items = []
    for item in items:
        news_item = {}
        news_item['title'] = item.title.text
        news_item['description']= item.description.text
        news_item['category']=item.category.text
        news_item['link'] = item.link.text
        news_item['pubDate'] = item.pubDate.text
        news_items.append(news_item)
    df_rss = pd.DataFrame(news_items,columns=['title','description', 'category','link','pubDate'])
    return df_rss 