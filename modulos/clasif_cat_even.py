import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model  import LinearRegression as LinReg
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.svm import LinearSVC
import numpy as np
from modulos import prepare_text
from spacy.lang.es.stop_words import STOP_WORDS

def model_cat():
    x_train, x_test, y_train, y_test = train_test_split(UARIV_DF['lemmatized'], cat_evento, test_size=0.20)
    # MODELO PARA LAS 4 CATEGORIAS PRINCIPALES
    pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words=stop_words_sp, sublinear_tf=True)),
                         ('chi',  SelectKBest(chi2, k=10000)),
                         ('clf', LinearSVC(C=1.0, penalty='l1', max_iter=3000, dual=False))])
    model = pipeline.fit(x_train, y_train)
    vectorizer = model.named_steps['vect']
    chi = model.named_steps['chi']
    clf = model.named_steps['clf']
    # Con ngram_range=(1,2) se le está diciendo al modelo que considere un conjunto de 2 palabras.
    return model

def model_type():
    x_train, x_test, y_train, y_test = train_test_split(UARIV_DF['lemmatized'], tipo_de_evento, test_size=0.20)
    # MODELO PARA LAS 14 TIPOS
    pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words=stop_words_sp, sublinear_tf=True)),
                         ('chi',  SelectKBest(chi2, k=10000)),
                         ('clf', LinearSVC(C=1.0, penalty='l1', max_iter=3000, dual=False))])
    model = pipeline.fit(x_train, y_train)
    vectorizer = model.named_steps['vect']
    chi = model.named_steps['chi']
    clf = model.named_steps['clf']
    # Con ngram_range=(1,2) se le está diciendo al modelo que considere un conjunto de 2 palabras.
    return model

with open('./Data/NoticiasDataV01.csv') as f:
    UARIV_DF=pd.read_csv(f, delimiter=';')
UARIV_DF['REVIEW'] = UARIV_DF['REVIEW'].astype(str)
UARIV_DF["REVIEW_clean"] = UARIV_DF["REVIEW"].apply(lambda x: prepare_text.formatingText(x))
UARIV_DF["REVIEW_stopword"] = UARIV_DF["REVIEW_clean"].apply(lambda x:  " ".join(prepare_text.deletestopwords(x)))
UARIV_DF['lemmatized'] = UARIV_DF["REVIEW_stopword"].apply(lambda x: prepare_text.lemmatizer(x)).apply(lambda x: prepare_text.formatingText(x))
stop_words_sp = STOP_WORDS
tipo_de_evento = UARIV_DF["TIP_EVEN"]
cat_evento = UARIV_DF["CAT_EVENTO"]