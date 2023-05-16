import streamlit as st
import pandas as pd
import ast
import numpy as np

st.title('PI Henry DSFT10')
st.subheader('Rigoberto Godoy Hernández')


# Importamos df CSV
df = pd.read_csv(r'movies_dataset.csv')

# Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0
df = df.fillna({"budget": 0, "revenue": 0})
#Los valores nulos del campo release date deben eliminarse.
df = df.dropna(subset=["release_date"])

# De haber fechas, deberán tener el formato AAAA-mm-dd, 
df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors='coerce') 

# además deberán crear la columna release_year donde extraerán el año de la fecha de estreno.
df['release_year'] = pd.to_datetime(df['release_date']).dt.strftime('%Y')
df['release_month'] = pd.to_datetime(df['release_date']).dt.strftime('%m')
# Rellenamos nulos con CEROS
df = df.fillna({"release_month": 0})
# Cambiamos a tipo INT
df['release_month'] = df['release_month'].astype(str).astype(int)
# Creando columna con dia de la semana
df['release_weekday'] = pd.to_datetime(df['release_date']).dt.strftime('%A')

# Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, 
# dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, deberá tomar el valor 0
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')

df['return'] = df['revenue'].div(df['budget'])
df = df.fillna({"return": 0})

# Eliminar las columnas que no serán utilizadas, video,imdb_id,adult,original_title,vote_count,poster_path y homepage.
# df.drop(['video', 'imdb_id', 'adult', 'original_title', 'vote_count', 'poster_path', 'homepage'], axis = 1, inplace=True)


# ----------------FUNCION 1.- peliculas_mes(mes)   ------------------------------------------------
# '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes
# (nombre del mes, en str, ejemplo 'enero') historicamente''' 
def peliculas_mes(mes): 
    mes = mes.capitalize()
    meses = {'Enero':1, 'Febrero':2, 'Marzo':3, 'Abril':4, 'Mayo':5, 'Junio':6,
             'Julio':7, 'Agosto':8, 'Septiembre':9, 'Octubre':10, 'Noviembre':11, 'Diciembre':12}
    respuesta = len(df[df['release_month'] == meses[mes]].index)
    return respuesta;

meses_list = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
            'Octubre', 'Noviembre', 'Diciembre']
st.text('1.- Función que retorna la cantidad de películas estrenadas por MES')
opcion_meses = st.selectbox('Selecciona el mes', meses_list)

st.write('La cantidad de películas estrenadas durante ', opcion_meses,' fue de ', peliculas_mes(opcion_meses))


# ----------------FUNCION 2.- peliculas_dia(dia_de_la_semana)   ------------------------------------------------
# '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia 
# (de la semana, en str, ejemplo 'lunes') historicamente''' 

def peliculas_dia(dia): 
    dia = dia.capitalize()
    dia_esp = {'Lunes':'Monday', 'Martes':'Tuesday', 'Miercoles':'Wednesday', 'Jueves':'Thursday',
               'Viernes':'Friday','Sabado':'Saturday', 'Domingo':'Sunday'}
    respuesta = len(df[df['release_weekday'] == dia_esp[dia]].index)
    return respuesta

dia_sem_list = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
st.text('2.- Función que retorna la cantidad de películas estrenadas por dia de la semana')
opcion_dia_sem = st.selectbox('Selecciona el dia de la semana', dia_sem_list)

st.write('La cantidad de películas estrenadas en ', opcion_dia_sem,' fue de ', peliculas_dia(opcion_dia_sem))


# ---------------- DESANIDAR COLUMNAS --------------------------------------------------------------------------

# Lista
def fetch_name(obj): 
    if isinstance(obj, str) and '{' in obj:
        L=[]
        for i in ast.literal_eval(obj):
            L.append(i['name']);
        return L

# Diccionarios
def fetch_name2(obj): 
    if isinstance(obj, str) and '{' in obj:
        # print(obj)
        dicc = ast.literal_eval(obj)
        return dicc['name']

df['genres']                = df['genres'].apply(fetch_name)
df['belongs_to_collection']  = df['belongs_to_collection'].apply(fetch_name2)
df['production_companies']  = df['production_companies'].apply(fetch_name)
df['production_countries']  = df['production_countries'].apply(fetch_name)
df['spoken_languages']  = df['spoken_languages'].apply(fetch_name)

df_paises_planos = df['production_countries'].dropna().tolist()
# iterating over the data
flat_list = list()
flat_list = []

for item in df_paises_planos:
    # appending elements to the flat_list
    flat_list = flat_list + item

# Eliminando valores duplicados 
list_paises_unicos = []
for x in flat_list:
    if x not in list_paises_unicos:
        list_paises_unicos.append(x)
    

# ----------------FUNCION 3.- peliculas_pais(pais)   ------------------------------------------------
# '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo''' 
# df de paises sustituyendo nulos con '0'
df_paises = df['production_countries'].fillna(value='0')

def peliculas_pais(pais): 
    # aplanando la lista de listas
    test = pd.Series([x for item in df_paises for x in item]).value_counts()
    return test[pais]


st.text('3.- Función que retorna la cantidad de películas producidas por pais')
opcion_pais = st.selectbox('Selecciona el pais', list_paises_unicos)

st.write('La cantidad de películas producidas en ', opcion_pais,' fue de ', peliculas_pais(opcion_pais))


# ----------------FUNCION 4.- coleccion(coleccion)   ------------------------------------------------
# '''Se ingresa la colección, retornando la cantidad de peliculas, ganancia total y promedio''' 
df_collection = df[['belongs_to_collection','revenue']]
df_collection = df_collection.dropna(subset=['belongs_to_collection'])


def coleccion(coleccion):
    cantidad = df_collection['belongs_to_collection'].value_counts()[coleccion]
    rev_total = df_collection.loc[df_collection['belongs_to_collection'] == coleccion, 'revenue'].sum()
    rev_prom =rev_total/cantidad
    return {'Cantidad de Películas':cantidad, 'Ganancia Total':rev_total, 'Ganancia Promedio':rev_prom}

list_collection = df_collection['belongs_to_collection'].dropna().tolist()
flat_list2 = list()
flat_list2 = []

for item2 in list_collection:
    # appending elements to the flat_list2
    flat_list2.append(item2)

# Eliminando valores duplicados 
list_collection_unique = []
for x in flat_list2:
    if x not in list_collection_unique:
        list_collection_unique.append(x)

st.text('4.- Función que retorna la cantidad de películas, ganancia total y promedio de una colección')
opcion_coleccion = st.selectbox('Selecciona la colección', list_collection_unique)

st.write('Los datos de la colección: ', opcion_coleccion,' son ', coleccion(opcion_coleccion))


# ----------------FUNCION 5.- productoras(productora)   ------------------------------------------------
# # '''Ingresas la productora, retornando la ganancia total y la cantidad de peliculas realizadas''' 

df_company = df[['production_companies','revenue']]
df_company = df_company.dropna(subset=['production_companies'])
df_company.index = range(len(df_company.index))

def productoras(productora):
    k_movies = 0
    rev_total = 0
    rev_prom = 0
    k_elem = 0
    rev_movie = 0
    
    for n in range (len(df_company)):
        for i in range (len(df_company['production_companies'][n])):
            if df_company['production_companies'][n][i] == productora:
                k_movies = k_movies +1
        if k_movies > 0:
            rev_prom = df_company['revenue'][n] / len(df_company['production_companies'][n])
        rev_total = rev_total + rev_prom
        
    return {'Ganancia Total':rev_total, 'Cantidad de Películas':k_movies}

list_companies = df_company['production_companies'].dropna().tolist()
flat_list2 = list()
flat_list2 = []

for item2 in list_companies:
    # appending elements to the flat_list2
    flat_list2 = flat_list2 + item2

# Eliminando valores duplicados 
list_companies_unique = []
for x in flat_list2:
    if x not in list_companies_unique:
        list_companies_unique.append(x)

st.text('5.- Función que retorna la ganancia total y la cantidad de películas que realizó una productora')
opcion_productora = st.selectbox('Selecciona la productora', list_companies_unique)

st.write('Los datos de la productora: ', opcion_productora,' son ', productoras(opcion_productora))



# ----------------FUNCION 6.- retorno(pelicula)   ------------------------------------------------
# # '''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo''' 

df_movie = df[['title','budget','revenue', 'release_year', 'return']]
df_movie = df_movie.dropna(subset=['title'])
df_movie.index = range(len(df_movie.index))

def retorno(pelicula): 
    inversion = df_movie.loc[df_movie['title'] == pelicula, 'budget'].item()
    ganancia = df_movie.loc[df_movie['title'] == pelicula, 'revenue'].item()
    retorno = df_movie.loc[df_movie['title'] == pelicula, 'return'].item()
    anio = df_movie.loc[df_movie['title'] == pelicula, 'release_year'].item()
    
    return {'Inversion':inversion, 'Ganacia':ganancia,'ROI':retorno, 'Año de estreno':anio}

list_movies = df_movie['title'].dropna().tolist()
flat_list2 = list()
flat_list2 = []

#for item2 in list_movies:
    # appending elements to the flat_list2
 #   flat_list2 = flat_list2 + item2

# Eliminando valores duplicados 
list_movies_unique = []
for x in list_movies:
    if x not in list_movies_unique:
        list_movies_unique.append(x)

st.text('6.- Función que retorna la inversión, la ganancia, el ROI y el año en el que se lanzó la película')
opcion_movie = st.selectbox('Selecciona la productora', list_movies_unique)

st.write('Los datos de la pelicula: ', opcion_movie,' son ', retorno(opcion_movie))
