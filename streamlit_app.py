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
col2.header('Painel de Monitoramento de Simulídeos')
col1.image('logo_estado (3).png', width=250)

# Carrega dados geoespaciais dos municípios do Rio Grande do Sul
municipios = gpd.read_file('https://raw.githubusercontent.com/camilarinaldi/CEVS/refs/heads/main/RS_Municipios_2021.json')

# Carrega dados geoespaciais das regiões de saúde
regioes_de_saude = gpd.read_file('https://raw.githubusercontent.com/camilarinaldi/CEVS/refs/heads/main/regioes_saude_rs.json')

# Carrega dados geoespaciais das coordenadorias do RS
coordenadorias = gpd.read_file('https://raw.githubusercontent.com/camilarinaldi/CEVS/refs/heads/main/RS_por_CRS.json')

# Carrega dados geoespaciais do novo arquivo .geojson
calhas = gpd.read_file('https://raw.githubusercontent.com/camilarinaldi/CEVS/refs/heads/main/coordenadas_calhas.geojson')

# Criar abas no painel
aba_sobre, aba_programa = st.tabs(['Sobre', 'Programa'])

with aba_sobre:
    # Adicionar título na aba
    st.header('O que são os Simulídeos?')
    
    # Criar colunas para organizar o layout
    coluna_texto, coluna_imagens = st.columns([2,3])

    with coluna_texto:
        st.markdown(
        """
        Os borrachudos pertencem à classe Insecta, ordem Diptera, subordem Nematocera,
        Infraordem Culicomorpha, Superfamilia Simulioidea, família Simuliidae. 
        
        **CARACTERÍSTICAS DE CADA FASE:**

        **Ovos** – Os ovos são de pequenas dimensões, com formato semitriangular, como os representados pela Figura 1. As fêmeas depositam os ovos em vários tipos de
        substratos submersos ou sobre a água (PEPINELLI, 2008). São colocados pelas fêmeas durante o dia, em massas de número variável, 
        podendo chegar a centenas (HAMADA; MARDINI, 2011). O período de incubação leva entre 4 a 6 dias dependendo da temperatura,
        e uma fêmea coloca em média 236,9 ovos em sua vida.

        **Larvas** – O estágio de larva apresenta uma forte cápsula cefálica, com um par de grandes
        leques filtradores que auxiliam na alimentação.

        **Pupas** - As larvas do último estádio da maioria das espécies de Simulídeos constroem
        um casulo completo (fixo a um substrato) durante o início do processo de pupação. O tempo
        necessário entre o início da pupação e a emergência do adulto depende de características
        ambientais, principalmente a temperatura da água e é intrínseco de cada espécie. Em geral,
        o período de pupação varia entre 1 e 2 semanas.

         **Adultos** - Na fase adulta os borrachudos medem entre 1 e 5 mm de comprimento, corpo robusto com diferentes cores escuras (pretos e marrons escuros). Algumas espécies
        apresentam coloração amarelo-alaranjado ou cinza-claro (HAMADA; MARDINI, 2001).
        """
        )

    with coluna_imagens:
        col1, col2 = st.columns(2)
        col1.image('figura 2.png', width=350, caption='Figura 1. Massa de ovos. Foto: Neusa Hamada, INPA-AM / Fonte: RIO GRANDE DO SUL (2006)')
        col2.image('figura 3.png', width=350, caption='Figura 2. Simulium orbitale. Fonte: RIO GRANDE DO SUL, 2006. Foto: Neusa Hamada INPA – Manaus -AM (2005)')
        col1.image('figura 4.png', width=350, caption='Figura 3. Pupas de Simulium pertinax. Fonte: RIO GRANDE DO SUL, 2006. Foto: Neusa Hamada INPA – Manaus - AM (2005)')
        col2.image('figura 1.png', width=350, caption='Figura 4. Simulium perflavum - Programa Estadual/ RS. Fonte: Edmilson dos Santos (DVAS/CEVS/SES-RS)')

with aba_programa:
      # Adicionar título na aba
    st.header('Como funciona o programa estadual?')

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
            name='Calhas',
            text=calhas['municipio'],  # Substitua 'municipio' pela coluna que contém o nome da cidade
            hoverinfo='text'
))

        ))

    # Configurar o layout do mapa
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center={'lat': -30.452349861219243, 'lon': -53.55320517512141},
            zoom=5.3
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=False,
        title="Mapa com Linhas e Pontos"
    )

    # Exibir o mapa no Streamlit
    st.plotly_chart(fig, use_container_width=True)
