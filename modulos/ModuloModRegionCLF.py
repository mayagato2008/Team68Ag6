import pandas as pd
import pickle
import numpy as np
import nltk

#from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import MultiLabelBinarizer
#from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
#from sklearn.multiclass import OneVsRestClassifier
#from sklearn.ensemble import RandomForestClassifier

from modulos import prepare_text
from modulos import find_location


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

### Función para convertir texto a array para incluir al modelo

def newpredictionDEP(text,maxlen,tokenizer):
    instance1 = tokenizer.texts_to_sequences(pd.Series(text))

    flat_list = []
    for sublist in instance1:
        for item in sublist:
            flat_list.append(item)

    flat_list = [flat_list]

    instance2 = pad_sequences(flat_list, padding='post', maxlen=maxlen)
    return instance2


def MODELOREGION(inst, loaded_model):
    instanceCLASS=''
    if pd.notnull(inst):
        # Se limpia el texto para ingresar al modelo
        inst = prepare_text.formatingText(inst)
        inst = prepare_text.deletestopwords(inst)
        inst = ' '.join(inst)
        #inst = formatingText(inst)
        inst = prepare_text.onlyWORDS(inst,stop_mundep)
        inst = ' '.join(inst)
        instance = inst
        ###### CARGAR AL MODELO LAS PALABRAS
        instance_pred = loaded_model.predict(newprediction(instance,9,tokenizer))
        instance_pred = prepare_text.convertprobtobin(instance_pred,0.30)
        instanceCLASS = lemod.inverse_transform(instance_pred)
        instanceCLASS = str(instanceCLASS).strip('[()]')
        instanceCLASS = prepare_text.formatingText(instanceCLASS)
    return instanceCLASS



def MODELODEPARTAMENTO(inst, modeloDepart):
    instanceCLASS=''
    if pd.notnull(inst):
        # Se limpia el texto para ingresar al modelo
        inst = prepare_text.formatingText(inst)
        inst = prepare_text.deletestopwords(inst)
        inst = ' '.join(inst)
        #inst = formatingText(inst)
        inst = prepare_text.onlyWORDS(inst,stop_mundep)
        inst = ' '.join(inst)
        instance = inst
        ###### CARGAR AL MODELO LAS PALABRAS
#        instance_pred = loaded_modelDEP.predict(newpredictionDEP(instance,9,tokenizerDEP))
#        modeloDepart = find_location.modelo_dep()
        instance_pred = modeloDepart.predict(newpredictionDEP(instance,9,tokenizerDEP))
        instance_pred = prepare_text.convertprobtobin(instance_pred,0.30)
        instanceCLASS = lemodDEP.inverse_transform(instance_pred)
        instanceCLASS = str(instanceCLASS).strip('[()]')
        instanceCLASS = prepare_text.formatingText(instanceCLASS)
    return instanceCLASS

with open('ModReg/COOR_DEP.csv') as f:
        COOR_DEP2=pd.read_csv(f, delimiter=',')


def val(DEPARTAMENTO):
    if DEPARTAMENTO =='':
        DEPARTAMENTO = 'archipielagodesanandres'
    else:
        DEPARTAMENTO = DEPARTAMENTO
    return DEPARTAMENTO

def LONGITUDE(instanceCLASS):
    instanceCLASS = val(instanceCLASS)
    instanceCLASS = instanceCLASS.split() # convert to list 
    instanceRES = pd.DataFrame(instanceCLASS, columns=['CODDEPAL'])
    COOR_DEP2["CODDEPAL"] = COOR_DEP2["CODDEPAL"].astype('object')
    COOR_DEP2["CODDEPAL"] = COOR_DEP2["CODDEPAL"].apply(lambda x: prepare_text.formatingText(x))
    COOR_DEP2["CODDEPAL"] = COOR_DEP2["CODDEPAL"].apply(lambda x: prepare_text.deletestopwords(x))
    COOR_DEP2['CODDEPAL'] = COOR_DEP2['CODDEPAL'].astype(str)
    COOR_DEP2["CODDEPAL"] = COOR_DEP2["CODDEPAL"].apply(lambda x: prepare_text.formatingText(x))
    #COOR_DEP2.head(3)
    instanceRES = pd.merge(instanceRES,COOR_DEP2, on='CODDEPAL')
    #instanceRES
    long = instanceRES['DEPlongitude'][0]
    return long


def LATITUDE(instanceCLASS):
    instanceCLASS = val(instanceCLASS)
    instanceCLASS = instanceCLASS.split() # convert to list 
    instanceRES = pd.DataFrame(instanceCLASS, columns=['CODDEPAL'])
    COOR_DEP2["CODDEPAL"] = COOR_DEP2["CODDEPAL"].astype('object')
    COOR_DEP2["CODDEPAL"] = COOR_DEP2["CODDEPAL"].apply(lambda x: prepare_text.formatingText(x))
    COOR_DEP2["CODDEPAL"] = COOR_DEP2["CODDEPAL"].apply(lambda x: prepare_text.deletestopwords(x))
    COOR_DEP2['CODDEPAL'] = COOR_DEP2['CODDEPAL'].astype(str)
    COOR_DEP2["CODDEPAL"] = COOR_DEP2["CODDEPAL"].apply(lambda x: prepare_text.formatingText(x))
    #COOR_DEP2.head(3)
    instanceRES = pd.merge(instanceRES,COOR_DEP2, on='CODDEPAL')
    #instanceRES
    lat = instanceRES['DEPlatitude'][0]
    return lat

#### CARGAR EL MODELO

##  Se crean las categorias para el modelo
## Dataframe with the name of categories
data = {'CODRegionlist2':  ['amazonia', 'andina', 'caribe', 'orinoquia', 'pacifico'] }
df = pd.DataFrame (data, columns = ['CODRegionlist2'])
   
df["CODRegionlist2"] = df["CODRegionlist2"].astype('object')
df["CODRegionlist2"] = df["CODRegionlist2"].apply(lambda x: prepare_text.formatingText(x))
df["CODRegionlist2"] = df["CODRegionlist2"].apply(lambda x: prepare_text.deletestopwords(x))
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

    
# loading CARGAR EL ARCHIVO DEL TOKENIZER
with open('ModReg/DEPtokenizermundep.pickle', 'rb') as handle:
    tokenizerDEP = pickle.load(handle)   


## CARGAR MODELO DE RANDOM FOREST

# load the model from disk
#filename = 'ModReg/MODclf.pkl'
#loaded_model = pickle.load(open(filename, 'rb'))
#result = loaded_model.score(X_test, Y_test)
#print(result)

## CREAR LAS VARIABLES PARA Y
lemod = MultiLabelBinarizer()
dfmod = lemod.fit_transform(df['CODRegionlist2'])




## Dataframe with the name of categories
data = {'CODDEPALlist2':  ['amazonas', 'antioquia', 'arauca', 'archipielagodesanandres',
       'atlantico', 'bogotadc', 'bolivar', 'boyaca', 'caldas', 'caqueta',
       'casanare', 'cauca', 'cesar', 'choco', 'cordoba', 'cundinamarca',
       'guainia', 'guaviare', 'huila', 'laguajira', 'magdalena', 'meta',
       'narino', 'nortedesantander', 'putumayo', 'quindio', 'risaralda',
       'santander', 'sucre', 'tolima', 'valledelcauca', 'vaupes',
       'vichada'] }


dfDEP = pd.DataFrame (data, columns = ['CODDEPALlist2'])
#dfDEP.head(5)

dfDEP["CODDEPALlist2"] = dfDEP["CODDEPALlist2"].astype('object')
#df["CODRegionlist2"] = df["CODRegionlist2"].apply(lambda x: formatingText(x))
dfDEP["CODDEPALlist2"] = dfDEP["CODDEPALlist2"].apply(lambda x: prepare_text.deletestopwords(x))
dfDEP['CODDEPALlist2'] = dfDEP['CODDEPALlist2'].astype(str)
dfDEP['CODDEPALlist2'] = dfDEP['CODDEPALlist2'].map(lambda x: eval(x))
dfDEP.head(3)


## CREAR LAS VARIABLES PARA Y DEPARTAMENTO
lemodDEP = MultiLabelBinarizer()
dfmodDEP = lemodDEP.fit_transform(dfDEP['CODDEPALlist2'])


## CARGAR MODELO DE DEPARTAMENTOS.

# load the model from disk
#filename = 'ModReg/DEPMODclf.pkl'
#loaded_modelDEP = pickle.load(open(filename, 'rb'))
#result = loaded_model.score(X_test, Y_test)
#print(result)

