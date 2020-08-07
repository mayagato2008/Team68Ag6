#import os
# EDA Pkgs
import pandas as pd
# web scrping Pkgs
import requests
from bs4 import BeautifulSoup

def web_scrp():
    #https://www.elheraldo.co/judicial
    # LEER LA PÁGINA JUDICIAL DEL MEDIO
    r = requests.get('https://www.elheraldo.co/judicial')
    # LLEVAR CÓDIGO HTML DE LA PÁGINA 
    soup = BeautifulSoup(r.text, 'html.parser')
    titulares = soup.find_all('article', attrs={'class':'item zoom'})
    rec_noticias = []
    # SE RECORREN TODOS LOS TITULARES Y SE ALMACENAN COMO REGISTROS INDIVIDUALES
    i=0
    medium_n='El Heraldo'
    category_n='Judicial'
    try:
        dfn = pd.read_csv('./data/news_ws.csv')
        i=dfn['id_not'].max()+1
    except Exception as error:
        pass
    for tit in titulares:
        nota_txt=tit.find('div', attrs={'class':'text'})
        link_n=nota_txt.find('h1').find('a')['href']
        #LEER LAS NOTICIAS UNA A UNA
        link_n='https://www.elheraldo.co'+link_n
        try:
            r = requests.get(link_n)
            soup2 = BeautifulSoup(r.text, 'html.parser')
            titulo_nota = soup2.find_all('title')
            title_n=titulo_nota[0].text.strip()
            pubDate_n = soup2.find("meta",  {"name":"cXenseParse:recs:publishtime"})
            pubDate_n = pubDate_n["content"] if pubDate_n else None
            desc_nota = soup2.find_all('div', attrs={'id':'body'})
            description_n=''
            description_n=desc_nota[0].text.strip()
            rec_noticias.append((i, title_n, description_n, pubDate_n, link_n, category_n, medium_n))
            i=i+1
        except Exception as error:
            pass
    # SE CONSTRUYE EL DATAFRAME CON LOS REGISTROS LEIDOS
    df_news = pd.DataFrame(rec_noticias, columns=['id_not','title', 'description', 'pubDate', 'link', 'category','medium'])
    df_news['pubDate'] = pd.to_datetime(df_news['pubDate'])
    # SE EXPORTA EL DATAFRAME A UN ARCHIVO "csv"
    with open('./data/news_ws.csv', 'a') as f:
        df_news.to_csv(f, header=False, index='id_not', encoding='utf-8')
    #df_news.to_csv('./data/news_ws.csv', index='id_not', encoding='utf-8')
    return df_news

def rss(url_media):
    url =url_media
#    url = "https://www.eltiempo.com/rss/justicia_conflicto-y-narcotrafico.xml"
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

