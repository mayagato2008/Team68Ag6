import pandas as pd
import os
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

# /////////////////
with open('./Data/NoticiasDataV01.csv') as f:
newsvic=pd.read_csv(f, delimiter=';')

newsvic["CODMUN"] = newsvic["CODMUN"].astype('category')
newsvic["CAT_EVENTO"] = newsvic["CAT_EVENTO"].astype('category')
newsvic["TIP_EVEN"] = newsvic["TIP_EVEN"].astype('category')

with open('./Data/COOR_MUN1.csv') as f:
    COOR_MUN=pd.read_csv(f, delimiter=',')
newsvic = pd.merge(newsvic,COOR_MUN, on='CODMUN')


### CAMBIA EL TIPO DE VARIABLE A STRING, se quitan

newsvic['REVIEW'] = newsvic['REVIEW'].astype(str)
newsvic["REVIEW"] = newsvic["REVIEW"].apply(lambda x: formatingText(x))
newsvic["REVIEW"] = newsvic["REVIEW"].apply(lambda x: deletestopwords(x))
newsvic['REVIEW'] = newsvic['REVIEW'].astype(str)
newsvic["REVIEW"] = newsvic["REVIEW"].apply(lambda x: formatingText(x))

with open('./Data/MunicipiosCoord.csv') as f:
    Mun=pd.read_csv(f, delimiter=',')
    
### Se limpian los nombres de municipios y departamentos
Mun["NombreMunC"] = Mun["NombreMun"].apply(lambda x: formatingText(x))
Mun["NombreDepC"] = Mun["NombreDep"].apply(lambda x: formatingText(x))
Mun["MunDepC"] = Mun["MunDep"].apply(lambda x: formatingText(x))
Mun["NombreMunCS"] = Mun["NombreMunC"].apply(lambda x: deletestopwords(x))
Mun["NombreDepCS"] = Mun["NombreDepC"].apply(lambda x: deletestopwords(x))
Mun["MunDepCS"] = Mun["MunDepC"].apply(lambda x: deletestopwords(x))
Mun['MunDepCSstr'] = Mun['MunDepCS'].astype(str)
Mun["MunDepCSstr2"] = Mun["MunDepCSstr"].apply(lambda x: formatingText(x))
# Quitar caracteres especiales, puntos comas, etc
Mun['NombreMunCSstr'] = Mun['NombreMunCS'].astype(str)
Mun["NombreMunCSstr2"] = Mun["NombreMunCSstr"].apply(lambda x: formatingText(x))

stop_mundep = convertdictionary(Mun['MunDepCSstr2'])
stop_mun = convertdictionary(Mun['NombreMunCSstr2'])

# Realizamos el cruce de variables entre el REVIEW y los municipios, para identificar posibles ubicaciones

newsvic["REVIEW_mundep"] = newsvic["REVIEW"].apply(lambda x: onlyWORDS(x,stop_mundep))
newsvic['REVIEW_mundep'] = newsvic['REVIEW_mundep'].astype(str)
newsvic['REVIEW_mundep'] = newsvic['REVIEW_mundep'].apply(lambda x: formatingText(x))
    