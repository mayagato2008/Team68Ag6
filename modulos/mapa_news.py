import pandas as pd
import os
import codecs
import base64
import matplotlib.pyplot as plt
import nltk
import re
from unicodedata import normalize
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words_sp = stopwords.words("spanish")


def mapa():
    return newsvic

## Funcion para quitar caracteres especiales
def formatingText(text):
	text = text.lower()
	text = re.sub('<.*?>', '', text)
	text = re.sub(':.*?:', '', text)
	text = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", text), 0, re.I)
	text = normalize( 'NFC', text)
	text = re.sub('[^a-z ]', '', text)
	return text

## FUNCIÓN DE QUITAR LOS STOPWORDS
#from unicodedata import normalize
stop_words_sp = stopwords.words("spanish")
def deletestopwords(text):
    word_tokens = nltk.word_tokenize(text)
    word_tokens_clean = [each for each in word_tokens if each.lower() not in stop_words_sp and len(each.lower()) > 2]
    return word_tokens_clean

#DEJAR LOS STOP WORDS
stop_words_sp = stopwords.words("spanish")
def onlystopwords(text):
    word_tokens = nltk.word_tokenize(text)
    word_tokens_clean = [each for each in word_tokens if each.lower() in stop_words_sp and len(each.lower()) > 1]
    return word_tokens_clean

with open('./Data/NoticiasDataV01.csv') as f:
    newsvic=pd.read_csv(f, delimiter=';')

newsvic["CODMUN"] = newsvic["CODMUN"].astype('category')
newsvic["CAT_EVENTO"] = newsvic["CAT_EVENTO"].astype('category')
newsvic["TIP_EVEN"] = newsvic["TIP_EVEN"].astype('category')

with open('./Data/COOR_MUN1.csv') as f:
    COOR_MUN=pd.read_csv(f, delimiter=',', encoding='latin-1')
newsvic = pd.merge(newsvic,COOR_MUN, on='CODMUN')



    
