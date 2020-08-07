import os
import streamlit as st 

# EDA Pkgs
import pandas as pd
import chardet 

# Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')
import seaborn as sns 

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
    # SE RECORREN TODOS LOS TITUALES Y SE ALMACENAN COMO REGISTROS INDIVIDUALES
    i=0
    for tit in titulares:
        nota_txt=tit.find('div', attrs={'class':'text'})
        url_nota=nota_txt.find('h1').find('a')['href']
        #LEER LAS NOTICIAS UNA A UNA
        url_nota='https://www.elheraldo.co'+url_nota
        try:
            r = requests.get(url_nota)
            soup2 = BeautifulSoup(r.text, 'html.parser')
            titulo_nota = soup2.find_all('title')
            tit_nota=titulo_nota[0].text.strip()
            fecha_nota = soup2.find("meta",  {"name":"cXenseParse:recs:publishtime"})
            fecha_nota = fecha_nota["content"] if fecha_nota else None
            desc_nota = soup2.find_all('div', attrs={'id':'body'})
            desc_text=''
            desc_text=desc_nota[0].text.strip()
            rec_noticias.append((i, tit_nota, fecha_nota, desc_text, url_nota))
            i=i+1
        except Exception as error:
            pass
    # SE CONSTRUYE EL DATAFRAME CON LOS REGISTROS LEIDOS
    df_noticias = pd.DataFrame(rec_noticias, columns=['id_not','titulo_nota', 'fecha_nota', 'desc_text', 'url_nota'])
    df_noticias['fecha_nota'] = pd.to_datetime(df_noticias['fecha_nota'])
    # SE EXPORTA EL DATAFRAME A UN ARCHIVO "csv"
    df_noticias.to_csv('./data/el_heraldo_judicial.csv', index='id_not', encoding='utf-8')
    return df_noticias

def main():
	st.image('unidadvictimas_logo2018-01.jpg', use_column_width=False)
#	""" Common ML Dataset Explorer """
	st.title("UARIV")
	st.subheader("Proyecto Data Science - DS4A Colombia 2.0")
	html_temp = """
	<div style="background-color:tomato;"><p style="color:white;font-size:15px;padding:8px">Automatic loading and classification of the daily event log (BDE) - Victims Attention and Repair Unit</p></div>
	"""
	st.markdown(html_temp,unsafe_allow_html=True)

	def file_selector(folder_path='./data'):
		filenames = os.listdir(folder_path)
		selected_filename = st.selectbox("Select A file",filenames)
		return os.path.join(folder_path,selected_filename)

	filename = file_selector()
	st.info("You Selected {}".format(filename))

	# Read Data
#	df = pd.read_csv(filename, delimiter=',')
	with open(filename, 'rb') as f:
		result = chardet.detect(f.read())  # or readline if the file is large
	df = pd.read_csv(filename, encoding=result['encoding'])
	st.dataframe(web_scrp())
#    df = pd.read_csv(filename, encoding='utf-8')
	# Show Dataset

	# Show Columns
#	if st.button("Column Names"):
#		st.write(df.columns)

	# Show Shape
#	if st.checkbox("Shape of Dataset"):
#		data_dim = st.radio("Show Dimension By ",("Rows","Columns"))
#		if data_dim == 'Rows':
#			st.text("Number of Rows")
#			st.write(df.shape[0])
#		elif data_dim == 'Columns':
#			st.text("Number of Columns")
#			st.write(df.shape[1])
#		else:
#			st.write(df.shape)

	# Select Columns
	if st.checkbox("Select Columns To Show"):
		all_columns = df.columns.tolist()
		selected_columns = st.multiselect("Select",all_columns)
#		new_df = df[selected_columns]
		st.dataframe(new_df)
	
	# Show Values
#	if st.button("Value Counts"):
#		st.text("Value Counts By Target/Class")
#		st.write(df.iloc[:,-1].value_counts())

	# Show Summary
	if st.checkbox("Summary"):
		st.write(df.describe().T)

	## Plot and Visualization

	st.subheader("Data Visualization")
	# Correlation
	# Seaborn Plot
	if st.checkbox("Correlation Plot[Seaborn]"):
		st.write(sns.heatmap(df.corr(),annot=True))
		st.pyplot()
        
	
	# Pie Chart
	if st.checkbox("Pie Plot"):
		all_columns_names = df.columns.tolist()
		if st.button("Generate Pie Plot"):
			st.success("Generating A Pie Plot")
			st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
			st.pyplot()

	# Count Plot
	if st.checkbox("Plot of Value Counts"):
		st.text("Value Counts By Target")
		all_columns_names = df.columns.tolist()
		primary_col = st.selectbox("Primary Columm to GroupBy",all_columns_names)
		selected_columns_names = st.multiselect("Select Columns",all_columns_names)
		if st.button("Plot"):
			st.text("Generate Plot")
			if selected_columns_names:
				vc_plot = df.groupby(primary_col)[selected_columns_names].count()
			else:
				vc_plot = df.iloc[:,-1].value_counts()
			st.write(vc_plot.plot(kind="bar"))
			st.pyplot()

	st.sidebar.image('ds4aColombia2.png', use_column_width=False)
	st.sidebar.header("Options")
	if st.sidebar.button("Media tracking"):
		if st.sidebar.checkbox("El Heraldo"):
			st.dataframe(web_scrp())
	st.sidebar.button("News clasification")
	st.sidebar.button("Heatmap")
#		st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
            
#    st.sidebar.info("Automatic loading and classification of the daily event log (BDE) - Victims Attention and Repair Unit - Victims' #Attention and Repair Unit")

#	st.sidebar.header("Get Datasets")
#	st.sidebar.markdown("[Common ML Dataset Repo]("")")

	st.sidebar.header("Team-68")
	st.sidebar.info("Nathalia Chaparro; Jesús Mannios; "\
            " Raul Cuervo; Juan García; "\
            " Rafael Nino; Jairo Maya")
#	st.sidebar.text("Built with Streamlit")
	st.sidebar.text("2020 - Maintained by Jairo Maya")
    
if __name__ == '__main__':
	main()