#Importação das bibliotecas 
import requests
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium, folium_static
import streamlit as st
import time
from altair import Chart
import plotly.figure_factory as ff
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
 
# Configurações da página
st.set_page_config(
    page_title="Simulídeos",
    page_icon="	:bug:",
    layout="wide",
    initial_sidebar_state='collapsed'
) 
col1, col2, col3 = st.columns([1,2,1])

col3.image('logo_cevs (1).png', width=150)
col2.markdown("<h1 style='text-align: center;'>Painel de Monitoramento de Simulídeos</h1>", unsafe_allow_html=True)
col1.image('logo_estado (3).png', width=250)

# Carrega dados geoespaciais dos municípios do Rio Grande do Sul
municipios = gpd.read_file('https://raw.githubusercontent.com/andrejarenkow/geodata/main/municipios_rs_CRS/RS_Municipios_2021.json')

# Carrega dados geoespaciais das regiões de saúde
regioes_de_saude = gpd.read_file('https://raw.githubusercontent.com/andrejarenkow/geodata/main/Regi%C3%B5es%20de%20Sa%C3%BAde/regioes.json')

# Carrega dados geoespaciais das coordenadorias do RS
coordenadorias = gpd.read_file('https://raw.githubusercontent.com/andrejarenkow/geodata/refs/heads/main/RS_por_CRS/RS_por_CRS.json')
