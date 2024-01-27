import streamlit as st
import pandas as pd
import numpy as np
import base64
import csv
import seaborn as sns
#
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as po
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import matplotlib.pyplot as plt
import plotly.express as px
import random
from PIL import Image
import plotly.figure_factory as ff
#Tudo que precisamos do util
from utils import (
    N_SELECTED,
    CESAR_LOGO,
    APP_TITLE,
    PAGE_TITLE,
    MC_LOGO,
    LOGO,
    BR_FLAG,
    US_FLAG,
    DADOS_GOV,
    )

#Título da página e o logo que aparecerá no Browser!!!
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=LOGO,
    layout="wide",
    initial_sidebar_state="expanded",
)

#st.title(APP_TITLE)
#st.image(CESAR_LOGO)

## Data Operations ##
df = pd.read_csv(DADOS_GOV)
## --------------- ##

## GLOBAL ##
selected_options = []

def png_to_base64(file_path):
    with open(file_path, "rb") as img_file:
        base64_encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return base64_encoded
    
#Inicio do dash
with st.sidebar:
    #icon = Image.open(MC_LOGO)
    st.image(MC_LOGO)
    #st.write("Visit our Website")
    st.markdown("<h3 style='text-align: center;'>Visit our Website</h3>", unsafe_allow_html=True)
    flc1, flc2, flc3, flc4= st.columns(4)
    with flc2:
        # FIXME: note que se usarmos a opção com st.image, não ficará centralizado!
        #        assim, escolho usar a opção de colocar imagens com Markdown.
        #st.image(BR_FLAG, width=30)
        mc_site_br = "https://www.mcdonalds.com.br/"  # Replace with your desired URL
        mc_site_us = "https://www.mcdonalds.com/us/en-us.html"

        st.markdown(
            f'<div style="display: flex; flex-direction: column; align-items: center;">'
            f'<a href="{mc_site_br}" target="_blank" onclick="open_link(\'{mc_site_br}\')"> '
            f'<img src="{BR_FLAG}" style="width: 30px;"></a>'
            f'</div>',
            unsafe_allow_html=True 
        )
    with flc3:
        # FIXME: note que se usarmos a opção com st.image, não ficará centralizado!
        #        assim, escolho usar a opção de colocar imagens com Markdown.
        #st.image(US_FLAG, width=30)
        st.markdown(
            f'<div style="display: flex; flex-direction: column; align-items: center;">'
            f'<a href="{mc_site_us}" target="_blank" onclick="open_link(\'{mc_site_us}\')"> '
            f'<img src="{US_FLAG}" style="width: 30px;"></a>'
            f'</div>',
            unsafe_allow_html=True
        )    

mcol1 = st.columns(1)
with st.container(): 
    #Montante pago por município pelo gov considerando todo o período
    vlr_pag_municipio = df.groupby(['NME_MUNICIPIO'])['VALOR_PAGO'].sum().reset_index().copy()

    #Analisando os top 50 municípios dos 495 municípios outliers
    outliers = vlr_pag_municipio.sort_values('VALOR_PAGO',ascending=False).head(50)

    # Criar aplicação Streamlit
    st.title('Rank dos top 50 outliers')

    # Selecionar a coluna para agrupar
    categoria = st.selectbox('Selecione a categoria:', ['Auxílio por mês', 'Auxílios por estados', 'Auxílios por município', 'Auxílios por Região'])
    #['MES_COMPETENCIA', 'UF', 'NME_MUNICIPIO', 'NME_REGIAO'])
    if categoria == 'Auxílio por mês':
         categoria = 'MES_COMPETENCIA'
    elif categoria == 'Auxílios por estados':
         categoria = 'UF' 
    elif categoria == 'Auxílios por município':
         categoria = 'NME_MUNICIPIO'  
    else: 
         categoria = 'NME_REGIAO'

    # Agrupar dados
    dados_agrupados = df.groupby(categoria)['VALOR_PAGO'].sum().reset_index()
    dados_agrupados = dados_agrupados.sort_values(by='VALOR_PAGO', ascending=False).tail(50)    

    # Gerar gráfico de barras usando seaborn e matplotlib
    fig, ax = plt.subplots()
    #por algum motivo eu não sei pq não está mostrando quando coloco ela na horizontal. Aí fiz essa gambiarra aqui só pra mostrar e pra tu tbm ver... 
    #não consegui entender pq não está mostrando
    if categoria == 'MES_COMPETENCIA':
        sns.barplot(x=categoria, y='VALOR_PAGO', data=dados_agrupados.head(50), order=dados_agrupados[categoria])
        ax.set_xlabel(categoria)
        ax.set_ylabel('VALOR_PAGO')
    else:
        sns.barplot(y=categoria, x='VALOR_PAGO', data=dados_agrupados.head(50), order=dados_agrupados[categoria])
        ax.set_ylabel(categoria)
        ax.set_xlabel('VALOR_PAGO')
        plt.rcParams.update({'font.size': 4})
    
    ax.set_title('Rank dos top 50 municípios outliers')
    plt.xticks(rotation=45)

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)