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
col1, col2, col3 = st.columns([1,4,1])

col3.image('logo_cevs (1).png', width=150)
col2.markdown("<h1 style='text-align: center;'>Painel de Monitoramento de Simulídeos</h1>", unsafe_allow_html=True)
col1.image('logo_estado (3).png', width=250)

# Carrega dados geoespaciais dos municípios do Rio Grande do Sul
municipios = gpd.read_file('https://raw.githubusercontent.com/camilarinaldi/CEVS/refs/heads/main/RS_Municipios_2021.json')

# Carrega dados geoespaciais das regiões de saúde
regioes_de_saude = gpd.read_file('https://raw.githubusercontent.com/camilarinaldi/CEVS/refs/heads/main/regioes_saude_rs.json')

# Carrega dados geoespaciais das coordenadorias do RS
coordenadorias = gpd.read_file('https://raw.githubusercontent.com/camilarinaldi/CEVS/refs/heads/main/RS_por_CRS.json')

# Carrega dados geoespaciais do novo arquivo .geojson
calhas = gpd.read_file('https://raw.githubusercontent.com/camilarinaldi/CEVS/refs/heads/main/coordenadas_calhas.geojson')

# Inicializar o mapa
fig = go.Figure()

# Adicionar linhas das coordenadorias
coordenadorias_boundaries = coordenadorias.boundary
for geom in coordenadorias_boundaries:
    if geom.geom_type == 'LineString':
        coords = list(geom.coords)
        fig.add_trace(go.Scattermapbox(
            lon=[c[0] for c in coords],
            lat=[c[1] for c in coords],
            mode='lines',
            line=dict(color='black', width=1),
            name='Coordenadorias'
        ))
    elif geom.geom_type == 'MultiLineString':
        for line in geom.geoms:
            coords = list(line.coords)
            fig.add_trace(go.Scattermapbox(
                lon=[c[0] for c in coords],
                lat=[c[1] for c in coords],
                mode='lines',
                line=dict(color='black', width=1),
                name='Coordenadorias'
            ))

# Adicionar pontos das calhas
if calhas.geometry.geom_type.isin(['Point']).all():
    calhas['lon'] = calhas.geometry.x
    calhas['lat'] = calhas.geometry.y
    fig.add_trace(go.Scattermapbox(
        lon=calhas['lon'],
        lat=calhas['lat'],
        mode='markers',
        marker=dict(size=6, color='blue'),
        name='Calhas'
    ))

# Configurar o layout do mapa
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        center={'lat': -30.452349861219243, 'lon': -53.55320517512141},
        zoom=5.3
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False,  # Desativa a exibição de legendas
    title="Mapa com Linhas e Pontos"
)

# Exibir o mapa no Streamlit
st.plotly_chart(fig)

