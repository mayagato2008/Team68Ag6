    # By Jairo Fernando Maya Benavides - mayagato2008@gmail.com 
    #    Jesús David Mannios Padilla - jesusmannios@gmail.com 
    #    Raul Esteban Cuervo Sastoque - raulecuervo@gmail.com 
    #    Rafael Antonio Nino Vargas - rafaelninov@gmail.com 
    #   Elsy Nathalia Chaparro Hernandez - enathaliach@gmail.com 

# Core Pkgs
import streamlit as st 

# EDA Pkgs
import pandas as pd 
import codecs
import base64
from io import BytesIO
import pickle

from pandas_profiling import ProfileReport
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#import geopandas
#from shapely.geometry import LineString
#from descartes import PolygonPatch
from streamlit_folium import folium_static
import folium

# Components Pkgs
import streamlit.components.v1 as components
from streamlit_pandas_profiling import st_profile_report

# Custome Component Fxn
import sweetviz as sv 

#Customer paks
from modulos import wsTeam68
#from modulos import mapa_news
from modulos import prepare_text
from modulos import clasif_cat_even
from modulos import ModuloModRegionCLF
from modulos import mapaconhead
from modulos import find_location


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index = False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="DataNews.xlsx">Download Excel file</a>' # decode b'abc' => abc



footer_temp = """

	 <!-- CSS  -->
	  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	  <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" type="text/css" rel="stylesheet" media="screen,projection"/>
	  <link href="static/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
	   <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">


	 <footer class="page-footer grey darken-4">
	    <div class="container" id="aboutapp">
	      <div class="row">
	        <div class="col l6 s12">
	          <h5 class="white-text">About Data Science Project - DS4A Colombia 2.0</h5>
	          <p class="grey-text text-lighten-4">Using Web scraping, Machine learning, Streamlit.</p>


	        </div>
	      
	   <div class="col l3 s12">
	          <h5 class="white-text">Connect With Me</h5>
	          <ul>
	            <a href="https://facebook.com/jcharistech" target="_blank" class="white-text">
	            <i class="fab fa-facebook fa-4x"></i>
	          </a>
	          <a href="https://gh.linkedin.com/in/jesiel-emmanuel-agbemabiase-6935b690" target="_blank" class="white-text">
	            <i class="fab fa-linkedin fa-4x"></i>
	          </a>
	          <a href="https://www.youtube.com/channel/UC2wMHF4HBkTMGLsvZAIWzRg" target="_blank" class="white-text">
	            <i class="fab fa-youtube-square fa-4x"></i>
	          </a>
	           <a href="https://github.com/Jcharis/" target="_blank" class="white-text">
	            <i class="fab fa-github-square fa-4x"></i>
	          </a>
	          </ul>
	        </div>
	      </div>
	    </div>
	    <div class="footer-copyright">
	      <div class="container">
	      Made by <a class="white-text text-lighten-3" href="#">Nathalia Chaparro & Jesús Mannios & Raúl Cuervo</a><br/>
	      <a class="white-text text-lighten-3" href="#">Rafael Nino & Jairo Maya</a>
	      </div>
	    </div>
	  </footer>

	"""

def main():
	"""Data Science Project - DS4A Colombia 2.0"""
	st.set_option('deprecation.showfileUploaderEncoding', False)
	st.image('unidadvictimas_logo2018-01.jpg', use_column_width=False)
	st.sidebar.image('ds4aColombia2.png', use_column_width=False)
	st.markdown('---')
	menu = ["Home","Overview","Media tracking","News classification","Event classification", "Heatmap","About"]
	choice = st.sidebar.selectbox("Options",menu)
	modeloDepart=None

    
# EDA
	if choice == "Overview":
		st.info("Overview")
		data_file2='./data/BASE_PREVENCION_EMERGENCIA_20190923.csv'
		if data_file2 is not None:
			df2 = pd.read_csv(data_file2, encoding='latin-1')
			profile = ProfileReport(df2)
			st_profile_report(profile)
		if st.button("Generate Sweetviz Report"):
			if data_file2 is not None:
				df2 = pd.read_csv(data_file2, encoding='latin-1')                    
				report = sv.analyze(df2)
				report.show_html()
				st_display_sweetviz("SWEETVIZ_REPORT.html")

# NEWS COLLECTOR
	elif choice == "Media tracking":
		media = ["See News","El Heraldo","El Tiempo","RSSS","El país","Otro"]
		choice2 = st.sidebar.selectbox("Medio",media)
		subtitulo=str("Media tracking - "+ choice2)
		st.info(subtitulo)
		data_file='./data/news_ws.csv'
		if choice2 == "See News":
			if data_file is not None:
				df = pd.read_csv(data_file)
				df= df.sort_values('pubDate',ascending=False)
				st.dataframe(df[['id_not', 'title', 'description', 'pubDate', 'link', 'category', 'medium']])
		elif choice2 == "El Heraldo":
			df = wsTeam68.web_scrp()
			st.dataframe(df[['id_not', 'title', 'description', 'pubDate', 'link', 'category', 'medium']])
		elif choice2 == "El Tiempo":
			df = wsTeam68.rss('https://www.eltiempo.com/rss/justicia_conflicto-y-narcotrafico.xml')
			st.dataframe(df[['id_not', 'title', 'description', 'pubDate', 'link', 'category', 'medium']])
		elif choice2 == "El país":
			st.info("News Classifier")
#			df = wsTeam68.rss('https://www.elpais.com.co/rss/judicial')
#			st.dataframe(df)
		if st.button("Export to excel"):
			if data_file is not None:
				df = pd.read_csv(data_file)
			st.markdown(get_table_download_link(df), unsafe_allow_html=True)

# CLASIFICACION DE EVENTO
	elif choice == "News classification":
		st.info("News Classifier")
		data_file='./data/news_ws.csv'
		if data_file is not None:
				df = pd.read_csv(data_file)
		if st.button("News classification"):
			if modeloDepart is None:
				modeloDepart = find_location.modelo_dep()
				filename = './ModReg/MODclf.pkl'
				loaded_model = pickle.load(open(filename, 'rb'))
			pred_cate=clasif_cat_even.model_cat()
			pred_type=clasif_cat_even.model_type()  
			df['category_event']=df['description'].apply(lambda x: pred_cate.predict([prepare_text.lemant(x)])[0])
			df['type_event']=df['description'].apply(lambda x: pred_type.predict([prepare_text.lemant(x)])[0])
			df['region']=df['description'].apply(lambda x: ModuloModRegionCLF.MODELOREGION(x, loaded_model))
			df['departamento']=df['description'].apply(lambda x: ModuloModRegionCLF.MODELODEPARTAMENTO(x, modeloDepart))    
			st.dataframe(df[['title','region','departamento','category_event','type_event','description']])
			df.to_csv('./data/news_ws_clas.csv', encoding='utf-8')
		if st.button("Export to excel"):
			data_file='./data/news_ws_clas.csv'            
			if data_file is not None:
				df = pd.read_csv(data_file)
			st.markdown(get_table_download_link(df), unsafe_allow_html=True)
		word_cloud_text = ''.join(df['description'].apply(lambda x: prepare_text.lemant(x)))
		wordcloud = WordCloud().generate(word_cloud_text)
		plt.figure()
		plt.axis("off")
		plt.imshow(wordcloud, interpolation="bilinear")
		plt.show()
		st.pyplot()


# CLASIFICACION DE EVENTO
	elif choice == "Event classification":
		st.info("Prediction with ML Clasification Model")
		news_text = st.text_area("Enter News Here","Type Here / Copy-paste")
		all_ml_models = ["Location - RFOREST","Category -SVM"]
		model_choice = st.selectbox("Select Model",all_ml_models)
		if st.button("Classify"):
			st.text("Original Text::\n{}".format(news_text))
#			vect_text = news_cv.transform([news_text]).toarray()
			if model_choice == 'Category -SVM':
				vect_text1 = prepare_text.lemant(news_text)
				predCateg=clasif_cat_even.model_cat()
				predType=clasif_cat_even.model_type()
				predi_categ = predCateg.predict([vect_text1])[0]
				predi_type = predType.predict([vect_text1])[0]
				st.write(f'Category - {predi_categ} - Type - {predi_type}')
			elif model_choice == 'Location - RFOREST':
				if modeloDepart is None:
					modeloDepart = find_location.modelo_dep()
					filename = './ModReg/MODclf.pkl'
					loaded_model = pickle.load(open(filename, 'rb'))
				pred_Region=ModuloModRegionCLF.MODELOREGION(news_text, loaded_model)
				pred_Departament=ModuloModRegionCLF.MODELODEPARTAMENTO(news_text, modeloDepart)
				pred_Lat=ModuloModRegionCLF.LATITUDE(pred_Departament)
				pred_Lon=ModuloModRegionCLF.LONGITUDE(pred_Departament)
				st.write(f'Región - {pred_Region} - Departamento - {pred_Departament}')
				st.write(f'Latitud - {pred_Lat} - Longitud {pred_Lat}')
				map=mapaconhead.HMAP(pred_Lat,pred_Lon)
				folium_static(map)


#NUEVA FUNCIONALIDAD DE CLASIF

	elif choice == "Heatmap":
		st.info("Mapa de hechos victimizantes")
#		data=mapa_news.mapa()
#		gdfCOL = geopandas.read_file('./Data/COL_adm/COL_adm0.shp')
#		gdfCOL.plot()
#		plt.scatter(data['longitude'],data['latitude'],color='purple')
#		st.pyplot()

	elif choice == "About":
		st.info("About App")
		components.html(footer_temp,height=500)

	else:
		html_temp = """
		<div style="background-color:royalblue;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Daily Events Log news collector and classification for a swift response action</h1>
		</div>
		"""

		components.html(html_temp)

		components.html("""

			<style>
			* {box-sizing: border-box}
			body {font-family: Verdana, sans-serif; margin:0}
			.mySlides {display: none}
			img {vertical-align: middle;}

			/* Slideshow container */
			.slideshow-container {
			  max-width: 1000px;
			  position: relative;
			  margin: auto;
			}

			/* Next & previous buttons */
			.prev, .next {
			  cursor: pointer;
			  position: absolute;
			  top: 50%;
			  width: auto;
			  padding: 16px;
			  margin-top: -22px;
			  color: white;
			  font-weight: bold;
			  font-size: 18px;
			  transition: 0.6s ease;
			  border-radius: 0 3px 3px 0;
			  user-select: none;
			}

			/* Position the "next button" to the right */
			.next {
			  right: 0;
			  border-radius: 3px 0 0 3px;
			}

			/* On hover, add a black background color with a little bit see-through */
			.prev:hover, .next:hover {
			  background-color: rgba(0,0,0,0.8);
			}

			/* Caption text */
			.text {
			  color: #f2f2f2;
			  font-size: 15px;
			  padding: 8px 12px;
			  position: absolute;
			  bottom: 8px;
			  width: 100%;
			  text-align: center;
			}

			/* Number text (1/3 etc) */
			.numbertext {
			  color: #f2f2f2;
			  font-size: 12px;
			  padding: 8px 12px;
			  position: absolute;
			  top: 0;
			}

			/* The dots/bullets/indicators */
			.dot {
			  cursor: pointer;
			  height: 15px;
			  width: 15px;
			  margin: 0 2px;
			  background-color: #bbb;
			  border-radius: 50%;
			  display: inline-block;
			  transition: background-color 0.6s ease;
			}

			.active, .dot:hover {
			  background-color: #717171;
			}

			/* Fading animation */
			.fade {
			  -webkit-animation-name: fade;
			  -webkit-animation-duration: 1.5s;
			  animation-name: fade;
			  animation-duration: 1.5s;
			}

			@-webkit-keyframes fade {
			  from {opacity: .4} 
			  to {opacity: 1}
			}

			@keyframes fade {
			  from {opacity: .4} 
			  to {opacity: 1}
			}

			/* On smaller screens, decrease text size */
			@media only screen and (max-width: 300px) {
			  .prev, .next,.text {font-size: 11px}
			}
			</style>
			</head>
			<body>

			<div class="slideshow-container">

			<div class="mySlides fade">
			  <div class="numbertext">1 / 3</div>
			  <img src="https://www.w3schools.com/howto/img_nature_wide.jpg" style="width:100%">
			  <div class="text">Caption Text</div>
			</div>

			<div class="mySlides fade">
			  <div class="numbertext">2 / 3</div>

			  <img src="https://www.w3schools.com/howto/img_snow_wide.jpg" style="width:100%">
			  <div class="text">Caption Two</div>
			</div>

			<div class="mySlides fade">
			  <div class="numbertext">3 / 3</div>
			  <img src="https://www.w3schools.com/howto/img_mountains_wide.jpg" style="width:100%">
			  <div class="text">Caption Three</div>
			</div>

			<a class="prev" onclick="plusSlides(-1)">&#10094;</a>
			<a class="next" onclick="plusSlides(1)">&#10095;</a>

			</div>
			<br>

			<div style="text-align:center">
			  <span class="dot" onclick="currentSlide(1)"></span> 
			  <span class="dot" onclick="currentSlide(2)"></span> 
			  <span class="dot" onclick="currentSlide(3)"></span> 
			</div>

			<script>
			var slideIndex = 1;
			showSlides(slideIndex);

			function plusSlides(n) {
			  showSlides(slideIndex += n);
			}

			function currentSlide(n) {
			  showSlides(slideIndex = n);
			}

			function showSlides(n) {
			  var i;
			  var slides = document.getElementsByClassName("mySlides");
			  var dots = document.getElementsByClassName("dot");
			  if (n > slides.length) {slideIndex = 1}    
			  if (n < 1) {slideIndex = slides.length}
			  for (i = 0; i < slides.length; i++) {
			      slides[i].style.display = "none";  
			  }
			  for (i = 0; i < dots.length; i++) {
			      dots[i].className = dots[i].className.replace(" active", "");
			  }
			  slides[slideIndex-1].style.display = "block";  
			  dots[slideIndex-1].className += " active";
			}
			</script>


			""")


if __name__ == '__main__':
	main()
