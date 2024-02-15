import streamlit as st
import pandas as pd
import numpy as np
import base64
import csv
import seaborn as sns
import json
#
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as po
import matplotlib.pyplot as plt
import plotly.express as px
import random
from PIL import Image
import plotly.figure_factory as ff
#Tudo que precisamos do util
from utils import (
    PAGE_TITLE,
    MC_LOGO,
    LOGO,
    BR_FLAG,
    DADOS_GOV,
    LOGO_GOV
    )

#Título da página e o logo que aparecerá no Browser!!!
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=LOGO,
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    st.markdown("<h3 style='text-align: center; color: white;'>Conheça mais sobre o PBF</h3>", unsafe_allow_html=True)
    flc1, flc2, flc3, flc4= st.columns(4)
    with flc2:
        # FIXME: note que se usarmos a opção com st.image, não ficará centralizado!
        #        assim, escolho usar a opção de colocar imagens com Markdown.
        #st.image(BR_FLAG, width=30)
        pbf_gov = "https://www.gov.br/mds/pt-br/acoes-e-programas/bolsa-familia"  # Replace with your desired URL
        site_gov = "https://www.gov.br/pt-br"

        st.markdown(
            f'<div style="display: flex; flex-direction: column; align-items: center;">'
            f'<a href="{site_gov}" target="_blank" onclick="open_link(\'{site_gov}\')"> '
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
            f'<a href="{pbf_gov}" target="_blank" onclick="open_link(\'{pbf_gov}\')"> '
            f'<img src="{LOGO_GOV}" style="width: 50px;"></a>'
            f'</div>',
            unsafe_allow_html=True
        )    

with st.container():
    
    vlr_pag_ano = df.groupby('ANO')['VALOR_PAGO'].sum().reset_index()

    #Montante pago por município pelo gov considerando todo o período
    vlr_pag_municipio = df.groupby(['NME_MUNICIPIO'])['VALOR_PAGO'].sum().reset_index().copy()

    #Analisando os top 50 municípios dos 495 municípios outliers
    outliers = vlr_pag_municipio.sort_values('VALOR_PAGO',ascending=False).head(50)

    # Criar aplicação Streamlit
    st.markdown("<h1 style='color: gray;'>Dados PBF do ano 2018 à 2021</h1>", unsafe_allow_html=True)


    # Selecionar a coluna para agrupar
   # Função para aplicar estilos CSS ao elemento select box
    def apply_style(width_px):
        script = f"""
        <style>
            .st-b5 {{
                background-color: #f0f0f0;
                color: black;
                width: {width_px}px;
                display: flex;
                justify-content: center;
            }}
            .st-b5 select {{
                width: {width_px}px;
            }}
            .st-ct {{
                width: {width_px}px !important;
            }}
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                var select = document.querySelector('.st-b5 select');
                select.addEventListener('click', function() {{
                    var dropdown = document.querySelector('.st-ct');
                    dropdown.style.width = '{width_px}px';
                }});
            }});
        </script>
        """
        st.markdown(script, unsafe_allow_html=True)

    # Aplica os estilos ao select box
    width_px = 500  # Largura do select box em pixels
    apply_style(width_px)

    # Opções do select box
    lista = ['Auxílio por ano', 'Auxílios por estados', 'Auxílios por município', 'Auxílios por Região']

    # Selecionar a categoria
    with st.markdown("<div class='st-b5'>", unsafe_allow_html=True):
        categoria = st.selectbox('', lista, key="my_selectbox")

    # Opções do select box
    #lista = ['Auxílio por ano', 'Auxílios por estados', 'Auxílios por município', 'Auxílios por Região']

    # Selecionar a categoria
    #categoria = st.selectbox('Selecione a categoria:', lista, key="my_selectbox")
    #['MES_COMPETENCIA', 'UF', 'NME_MUNICIPIO', 'NME_REGIAO'])
    if categoria == 'Auxílio por ano':
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

    if categoria == 'MES_COMPETENCIA':
        vlr_pag_ano = df.groupby('ANO')['VALOR_PAGO'].sum().reset_index()
        pag_ano_bar = px.bar(vlr_pag_ano,
                            x='ANO',
                            y='VALOR_PAGO',
                            template='plotly_white',
                            labels={'ANO':'Ano', 'VALOR_PAGO':'Valor acumulado'},
                            barmode='relative',
                            color='VALOR_PAGO',
                            color_continuous_scale='viridis',
                            width=800,
                            height=700)

        # Configurações do eixo x
        pag_ano_bar.update_xaxes(title='Ano', title_font_color='gray', ticks='outside', tickfont_color='gray')

        # Configurações do eixo y
        pag_ano_bar.update_yaxes(title='Valor acumulado (R$)', ticks='outside', title_font_color='gray', tickfont_color='gray')

        # Configurações do layout
        pag_ano_bar.update_layout(title={'text':'Valor pago por ano pelo programa Bolsa Família', 'y':0.97, 'x':0.23}, title_font_color='gray')

        # Mostra o gráfico interativo no Streamlit
        st.plotly_chart(pag_ano_bar)

    elif categoria == 'NME_MUNICIPIO':
        #Analisando os top 50 municípios dos 495 municípios outliers
        outliers = vlr_pag_municipio.sort_values('VALOR_PAGO',ascending=False).head(50)
        pag_municipios_outliers_bar = px.bar(outliers,
                                             x='VALOR_PAGO',
                                             y='NME_MUNICIPIO',
                                             orientation='h',
                                             template='plotly_white',
                                             labels={'NME_MUNICIPIO':'Município','VALOR_PAGO':'Valor acumulado (R$)'},
                                             color='VALOR_PAGO',
                                             color_continuous_scale='viridis',
                                             width=1000,
                                             height=850)
        pag_municipios_outliers_bar.update_xaxes(title='Valor acumulado (R$)', title_font_color='gray', ticks='outside',tickfont_color='gray')
        pag_municipios_outliers_bar.update_yaxes(title='Municípios',ticks='outside', title_font_color='gray',tickfont_color='gray')
        pag_municipios_outliers_bar.update_layout(yaxis = {'categoryorder':'total ascending'},title={'text':'Valor acumulado por estado pago pelo pragrama Bolsa Família','y':0.97,'x':0.5},title_font_color='gray')

        pag_municipios_outliers_bar.update_layout(yaxis = {'categoryorder':'total ascending'},
                                                  title={'text':'Rank dos top 50 outliers por município',
                                                         'y':0.97,'x':0.35}) 
        st.plotly_chart(pag_municipios_outliers_bar)

    elif categoria == 'NME_REGIAO':
        vlr_pag_regiao = df.groupby(['NME_REGIAO'])['VALOR_PAGO'].sum().reset_index().copy()

        #configurando o gráfico
        pag_regiao_bar = px.bar(vlr_pag_regiao,
                                x='VALOR_PAGO',
                                y='NME_REGIAO',
                                orientation='h',
                                template='plotly_white',
                                labels={'VALOR_PAGO':'Valor acumulado (R$)', 'NME_REGIAO':'Região'},
                                color='VALOR_PAGO',
                                color_continuous_scale='viridis',
                                width=1000,
                                height=650)

        # Configurações do eixo x
        pag_regiao_bar.update_xaxes(title='Valor acumulado (R$)', title_font_color='gray', ticks='outside', tickfont_color='gray')

        # Configurações do eixo y
        pag_regiao_bar.update_yaxes(title='Macro região', ticks='outside', title_font_color='gray', tickfont_color='gray')

        # Configurações do layout
        pag_regiao_bar.update_layout(yaxis = {'categoryorder':'total ascending'},
                                    title={'text':'Valor acumulado por macro região pago pelo programa Bolsa Família', 'y':0.97, 'x':0.25},
                                    title_font_color='gray')

        # Mostra o gráfico interativo no Streamlit
        st.plotly_chart(pag_regiao_bar)


    elif categoria == 'UF':
        #Montante pago por estado pelo gov considerando todo o período
        vlr_pag_uf = df.groupby(['UF'])['VALOR_PAGO'].sum().reset_index()
        fig = px.bar(vlr_pag_uf.sort_values('VALOR_PAGO', ascending=False), 
                    x='VALOR_PAGO', 
                    y='UF', 
                    title='Valor total pago por estado ao cidadão inscrito no programa Bolsa Família no período de 2018 a 2021',
                    labels={'VALOR_PAGO': 'Valor pago', 'UF': 'Estados'},
                    color='VALOR_PAGO',
                    color_continuous_scale='viridis',
                    orientation='h',
                    width=900,
                    height=700)


        fig.update_layout(yaxis = {'categoryorder':'total ascending'},
                                    title={'text':'Valor acumulado por estado pago pelo programa Bolsa Família', 'y':0.97, 'x':0.23},
                                    title_font_color='gray')
        st.plotly_chart(fig)