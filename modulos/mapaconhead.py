
# Load relevant packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as sm
import warnings

#warnings.filterwarnings("ignore")  # Suppress all warnings

import numpy                 as np
import pandas                as pd
import matplotlib.pyplot     as plt
import seaborn               as sns
import sklearn.metrics       as Metrics
import pandas                as pd
import matplotlib.pyplot     as plt


import folium  #needed for interactive map
from folium.plugins import HeatMap

from   collections           import Counter
from   sklearn               import preprocessing
from   datetime              import datetime
from   collections           import Counter
from   math                  import exp
from   sklearn.linear_model  import LinearRegression as LinReg
from   sklearn.metrics       import mean_absolute_error
from   sklearn.metrics       import median_absolute_error
from   sklearn.metrics       import r2_score

#%matplotlib inline
#sns.set()

## leer la base de datos

def HMAP(LAT,LONG):
    with open('Data/NoticiasDataV01.csv') as f:
        newsvic10=pd.read_csv(f, delimiter=';')
    
    with open('Data/COOR_MUN1.csv') as f:
        COOR_MUN10=pd.read_csv(f, delimiter=',')
    COOR_MUN10.head(3)
    newsvic10 = pd.merge(newsvic10,COOR_MUN10, on='CODMUN') 

#max_amount = float(newsvic['COD_HECHO'].max())

### CREAR EL MAPA

    folium_hmap = folium.Map(width=700,height=700,
                            location=[4.688, -74.02],
                            zoom_start=6,
                            tiles="OpenStreetMap")
    max_amount = 10
    hm_wide = HeatMap( list(zip(newsvic10['latitude'], newsvic10['longitude'])),
                       min_opacity=0.2,
                       max_val=max_amount,
                       radius=10, blur=6, 
                       max_zoom=15, 
                     )

    folium_hmap = folium_hmap.add_child(hm_wide)
    marker = folium.CircleMarker(location=[LAT,LONG],radius=5,color="red",fill=True)
    marker.add_to(folium_hmap)
    return folium_hmap










