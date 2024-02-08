import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as po
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px
import random
import plotly.figure_factory as ff
from utils import LOGO, PAGE_TITLE, DADOS_GOV, MC_LOGO, BR_FLAG, LOGO_GOV
import base64
from pathlib import Path
import json

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


#Título da página e o logo que aparecerá no Browser!!!
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=LOGO,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Mapa")

with st.sidebar:
    #icon = Image.open(MC_LOGO)
    st.image(MC_LOGO)
    #st.write("Visit our Website")
    st.markdown("<h3 style='text-align: center;'>Conheça mais sobre o PBF</h3>", unsafe_allow_html=True)
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

## Data Operations ##
basegov = pd.read_csv(DADOS_GOV)
with open('C:\\Projetos\\Dash\\dash-auxilio-gov\\data\\uf.json', 'r', encoding='latin-1') as f:
    brasil = json.load(f)

# Para a leitura do mapa é necessário que a chave id tenha o mesmo valor da base.
# Para isso iterei pela chave features e inseri em id o valor da cheve 'UF_05'
for i in range(len(brasil['features'])):
    brasil['features'][i]['id'] = brasil['features'][i]['properties']['UF_05']

basegov2 = basegov
#Criando uma coluna com os dados da UF (primeiros dois numeros)
#brasil2["COD_UF"] = brasil2["id_municipio"].str[0:2]
basegov2 = basegov2.rename(columns={'COD_UF': 'UF'})

#Filtrando o dataframe para utilizar apenas um mês como referência
mensal = basegov2[(basegov2['MES'] == 1)]

#CRIANDO CÓDIGO PARA OS ESTADOS!
estados  =  {11: "RO", 12: 'AC',13:"AM",14:"RR",15:"PA",16:"AP",17:"TO",21:"MA",22:"PI",23:"CE",
             24:"RN",25:"PB",26:"PE",27:"AL",28:"SE",29:"BA",31:"MG",32:"ES",33:"RJ",35:"SP",
             41:"PR",42:"SC",43:"RS",50:"MS",51:"MT",52:"GO",53:"DF"}
#invertendo as posicoes do estado, pelo código.
estados = {v: k for k, v in estados.items()}

basegov2 = basegov2.rename(columns={'COD_UF': 'UF'})
basegov2['COD_UF'] = basegov2['UF'].map(estados)

# Calcular a soma de 'VALOR_PAGO' para cada combinação de 'ANO' e 'UF'
basegov2['SOMA_ANUAL'] =  basegov2.groupby(['ANO', 'UF'])['VALOR_PAGO'].transform('sum')

# Atribuir os resultados à nova coluna 'SOMA_ANUAL'
#basegov2['SOMA_ANUAL'] = soma_anual_uf

basegov2_ordem_crescente = basegov2.sort_values(by='ANO')

#basegov2['SOMA_ANUAL'] = soma_por_ano_uf

with st.container():

# Criação do gráfico 
    
    def criar_mapa(basegov2_ordem_crescente, brasil):
        fig = px.choropleth_mapbox(
        basegov2_ordem_crescente, # selecionando a base
        mapbox_style = "carto-positron", #selecionando o tipo de cartografia
        locations = 'UF', # A coluna do DF que será relacionada com JSON
        geojson = brasil, #A fonte do JSON
        color = "SOMA_ANUAL", #Valores que definirão a cor do gráfico
        hover_name = 'UF', #Informação que aparecerá no box
        hover_data = ["SOMA_ANUAL"], # Informação extra para aparecer no box
        title = "Percentual de valor destinado a famílias do PBF em relação à população (estimativa IBGE 2018 a 2021) por estado", # Titulo
        center={"lat": -14, "lon": -55}, # Centralização inicial do gráfico
        zoom=3.0,  # Zoom inicial do gráfico
        animation_frame = 'ANO', # Coluna que será iterada para a animação
        opacity = 0.6 ,
        color_continuous_scale='reds')
        fig.update_layout(height=700, width = 1000)
        return fig

figura_do_mapa = criar_mapa(basegov2_ordem_crescente, brasil)
st.plotly_chart(figura_do_mapa)