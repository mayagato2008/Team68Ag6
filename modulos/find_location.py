import pandas as pd
import pickle
import numpy as np
import nltk

from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier

from modulos import prepare_text

def modelo_dep():
    le = MultiLabelBinarizer()
    yn1 = le.fit_transform(newsvic['CODDEPALlist2'])
    X_train1, X_test1, y_train1, y_test1 = train_test_split(newsvic['REVIEW_mundep'], yn1,  test_size=0.20, random_state=0)
    X_train1T = tokenizer.texts_to_sequences(X_train1)
    X_test1T = tokenizer.texts_to_sequences(X_test1)
    vocab_size = len(tokenizer.word_index) + 1
    maxlen = 9
    X_train1T9 = pad_sequences(X_train1T, padding='post', maxlen=maxlen)
    X_test1T9 = pad_sequences(X_test1T, padding='post', maxlen=maxlen)
    DEPmodel1 = OneVsRestClassifier(RandomForestClassifier(n_jobs=-1, n_estimators=500, max_depth=100, random_state=42))
    DEPmodel1.fit(X_train1T9, y_train1)
    return DEPmodel1

def newpredictionDEP(text,maxlen,tokenizer):
    instance1 = tokenizer.texts_to_sequences(pd.Series(text))
    flat_list = []
    for sublist in instance1:
        for item in sublist:
            flat_list.append(item)
    flat_list = [flat_list]
    instance2 = pad_sequences(flat_list, padding='post', maxlen=maxlen)
    return instance2


with open('./data/news_vic_aj.csv') as f:
    newsvic=pd.read_csv(f)
newsvic['REVIEW_mundep'] = newsvic['REVIEW_mundep'].astype(str)
newsvic['CODDEPALlist2'] = newsvic['CODDEPALlist'].map(lambda x: eval(x))

with open('ModReg/DEPtokenizermundep.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
