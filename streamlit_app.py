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
    page_title="Ovitrampas",
    page_icon="	:bug:",
    layout="wide",
    initial_sidebar_state='collapsed'
) 
col1, col2, col3 = st.columns([1,4,1])

col3.image('logo_cevs (1).png', width=150)
col2.header('Painel de Monitoramento de Aedes aegypti através de Ovitrampas')
col1.image('logo_estado (3).png', width=250)
