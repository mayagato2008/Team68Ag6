import pandas as pd
import numpy as np
import nltk # imports the natural language toolkit
from nltk.corpus import stopwords
from nltk import word_tokenize
nltk.download('stopwords')
#from spacy.lang.es.stop_words import STOP_WORDS
import re
from unicodedata import normalize
#import es_core_news_sm

#def is_nan(x):
#    return (x is np.nan or x != x)


def deletestopwords(text):
    word_tokens_clean=[' ']
    if pd.notnull(text):
        word_tokens = nltk.word_tokenize(text)
    #     stop_words_sp = set(stopwords.words("spanish"))
    #    stop_words_sp = STOP_WORDS # WITH SPACY
        stop_words_sp.append("ao")
        word_tokens_clean = [each for each in word_tokens if each.lower() not in stop_words_sp]
#                             and len(each.lower()) > 2]
    return word_tokens_clean


def deletestopwords2(text):
# Se colocan estas palabras para que las borre, como si fueran stopwords
    stop_words_sp.append('nacional') 
    stop_words_sp.append('colombia')
    word_tokens_clean=[' ']
    if pd.notnull(text):
        word_tokens = nltk.word_tokenize(text)
    #     stop_words_sp = set(stopwords.words("spanish"))
    #    stop_words_sp = STOP_WORDS # WITH SPACY
        stop_words_sp.append("ao")
        word_tokens_clean = [each for each in word_tokens if each.lower() not in stop_words_sp]
#                             and len(each.lower()) > 2]
    return word_tokens_clean


def onlystopwords(text):
    word_tokens_clean=[' ']
    if pd.notnull(text):
        word_tokens = nltk.word_tokenize(text)
        word_tokens_clean = [each for each in word_tokens if each.lower() in stop_words_sp and len(each.lower()) > 1]
    return word_tokens_clean

def onlyWORDS(text,WORDS):
    word_tokens_clean=[' ']
    if pd.notnull(text):
        word_tokens = nltk.word_tokenize(text)
        word_tokens_clean = [each for each in word_tokens if each in WORDS]
    return word_tokens_clean


# Función para convertir a diccionario texto
def convertdictionary(columntext):
    token_lists = [word_tokenize(each) for each in columntext]
    tokens = [item for sublist in token_lists for item in sublist]
    return tokens


def lemmatizer(text):  
  doc = nlp(text)
  return ' '.join([word.lemma_ for word in doc])


def formatingText(text):
    if pd.notnull(text):
        text = text.lower()
        text = re.sub('<.*?>', '', text)
        text = re.sub(':.*?:', '', text)
        text = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", text), 0, re.I)
        text = normalize( 'NFC', text)
        text = re.sub('[^a-z ]', '', text)
    return text


def lemant(text1):
    if pd.notnull(text1):
        x=text1.lower()
        stopwords= deletestopwords(x)
        stopwords=str(stopwords)
        clean = formatingText(stopwords)
        final = lemmatizer(clean)
    else:
        final =' '
    return final

def convertprobtobin(array,threshold):
    num_rows = np.shape(array)[0]
    num_columns = np.shape(array)[1]
    z2 = array
    n=num_columns # Número de columnas
    p=num_rows # Número de filas
    i=0
    j=0
    for i in range(p):
        for j in range(n):
            if array[i,j] < threshold:
                z2[i][j] = 0
            else:
                z2[i][j] = 1
    threshold = 0            
    return array

def espacios(text1):
#    text1=text1.replace(' ','')
    text1=re.sub(r'\s+', '', text1)
#    re.sub(r'\s', '', text1)
#    text1.translate(str.maketrans('', '', string.whitespace))
    return text1

nlp = es_core_news_sm.load()
nltk.download('stopwords')
stop_words_sp = stopwords.words("spanish")
