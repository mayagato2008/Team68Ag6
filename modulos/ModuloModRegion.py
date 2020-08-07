import pandas as pd

import numpy as np

import re

from unicodedata import normalize

def formatingTextTEST1(text):
	text = text.lower()
	text = re.sub('<.*?>', '', text)
	text = re.sub(':.*?:', '', text)
	text = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", text), 0, re.I)
	text = normalize( 'NFC', text)
	text = re.sub('[^a-z ]', '', text)
	return text



import numpy as np
import pandas as pd

import pandas as pd
import numpy as np
import tensorflow as tf
import re
import nltk
from nltk.corpus import stopwords

import pickle

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from tensorflow.keras import regularizers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, GlobalMaxPooling1D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping

try:
    tf.set_random_seed(1337)                    # set the random seed for reproducibility
except:
    tf.random.set_seed(1337)                     # NOTE: Newer version of tensorflow uses tf.random.set_seed
np.random.seed(1337)   



nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words_sp = stopwords.words("spanish")

from unicodedata import normalize


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
# http://zetcode.com/lang/python/lists/
stop_words_sp = stopwords.words("spanish")
stop_words_sp.append("nacional") # Se colocan estas palabras para que las borre, como si fueran stopwords
stop_words_sp.append("colombia")

#stop_words_sp.insert(0, "PHP")
#stop_words_sp.insert(1, "Lua")

def deletestopwords(text):
    stop_words_sp = stopwords.words("spanish")
    stop_words_sp.append('nacional') # Se colocan estas palabras para que las borre, como si fueran stopwords
    stop_words_sp.append('colombia')
    word_tokens = nltk.word_tokenize(text)
    word_tokens_clean = [each for each in word_tokens if each.lower() not in stop_words_sp and len(each.lower()) > 2]
    return word_tokens_clean

#DEJAR LOS STOP WORDS
    stop_words_sp = stopwords.words("spanish")
    stop_words_sp.append('nacional') # Se colocan estas palabras para que las borre, como si fueran stopwords
    stop_words_sp.append('colombia')


def onlystopwords(text):
    stop_words_sp = stopwords.words("spanish")
    stop_words_sp.append('nacional') # Se colocan estas palabras para que las borre, como si fueran stopwords
    stop_words_sp.append('colombia')
    word_tokens = nltk.word_tokenize(text)
    word_tokens_clean = [each for each in word_tokens if each.lower() in stop_words_sp and len(each.lower()) > 1]
    return word_tokens_clean


# Función para convertir a diccionario texto
def convertdictionary(columntext):
    token_lists = [word_tokenize(each) for each in columntext]
    tokens = [item for sublist in token_lists for item in sublist]
    return tokens


## FUNCIÓN PARA FILTRAR LOS MUNICIPIOS Y LOS DEPARTAMENTOS
def onlyWORDS(text,WORDS):
    word_tokens = nltk.word_tokenize(text)
    #WORDS_tokens = nltk.word_tokenize(WORDS)
    #word_tokens_clean = [each for each in word_tokens if each.lower() in WORDS and len(each.lower()) > 1]
    word_tokens_clean = [each for each in word_tokens if each in WORDS]
    return word_tokens_clean

### Función para convertir texto, la  variable x al array para incluir al modelo

def newprediction(text,maxlen,tokenizer):
    instance1 = tokenizer.texts_to_sequences(pd.Series(text))

    flat_list = []
    for sublist in instance1:
        for item in sublist:
            flat_list.append(item)

    flat_list = [flat_list]

    instance2 = pad_sequences(flat_list, padding='post', maxlen=maxlen)
    return instance2


## FUNCIÓN PARA CONVERTIR LOS VALORES DE PROBABILIDAD EN 1 Y 0
## la entrada es un ARRAY


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



#### CARGAR EL MODELO

from keras.models import model_from_json

##  Se crean las categorias para el modelo
## Dataframe with the name of categories
data = {'CODRegionlist2':  ['amazonia', 'andina', 'caribe', 'orinoquia', 'pacifico'] }
df = pd.DataFrame (data, columns = ['CODRegionlist2'])
   
df["CODRegionlist2"] = df["CODRegionlist2"].astype('object')
df["CODRegionlist2"] = df["CODRegionlist2"].apply(lambda x: formatingText(x))
df["CODRegionlist2"] = df["CODRegionlist2"].apply(lambda x: deletestopwords(x))
df['CODRegionlist2'] = df['CODRegionlist2'].astype(str)
df['CODRegionlist2'] = df['CODRegionlist2'].map(lambda x: eval(x))



## leer archivo spara el modelo
### CARGAR BIBLIOTECA DE MUNICIPIOS Y DEPARTAMENTO
with open ('ModReg/stop_mundep.txt', 'rb') as fp:
    list_1 = pickle.load(fp)
stop_mundep = list_1  

# loading CARGAR EL ARCHIVO DEL TOKENIZER
with open('ModReg/tokenizermundep.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load json and create model
json_file = open('ModReg/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("ModReg/model.h5")
#print("Loaded model from disk")

# Se compila nuevamente el modelo
# evaluate loaded model on test data
loaded_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
#loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

## CREAR LAS VARIABLES PARA Y
lemod = MultiLabelBinarizer()
dfmod = lemod.fit_transform(df['CODRegionlist2'])



def MODELOREGION(inst):
    # Se limpia el texto para ingresar al modelo
    inst = formatingText(inst)
    inst = deletestopwords(inst)
    inst = ' '.join(inst)
    #inst = formatingText(inst)
    inst = onlyWORDS(inst,stop_mundep)
    inst = ' '.join(inst)
    instance = inst
    ###### CARGAR AL MODELO LAS PALABRAS
    instance_pred = loaded_model.predict(newprediction(instance,9,tokenizer))
    instance_pred = convertprobtobin(instance_pred,0.30)
    instanceCLASS = lemod.inverse_transform(instance_pred)
    return instanceCLASS
