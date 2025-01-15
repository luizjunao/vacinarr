import streamlit as st
import pandas as pd
import plotly.express as px


# Título da página
st.title("Relatório de Doenças de Notificação Compulsória")

# Função para carregar a base de dados
@st.cache_data
def carregar_dados():
    return pd.read_csv(r"C:\Users\SESAU-RR\Python\Pessoal\monit_dnc\dados\notindiv.csv")

# Carregar a base de dados
base = carregar_dados()

# Filtrar os dados para o estado de Roraima
base_rr = base[base['SG_UF_NOT'] == 14]

# Converter a coluna data_not para o formato de data
base_rr['DT_NOTIFIC'] = pd.to_datetime(base_rr['DT_NOTIFIC'], errors='coerce')


# Container dos filtros e gráficos
with st.container():
    col1, col2, col3 = st.columns([1, 1, 2]) 
    with col1:
        anos = ['Todos'] + list(base_rr['NU_ANO'].astype(str).unique())
        ano_selecionado = st.selectbox("Selecione o Ano", anos)
    with col2:
        municipios = ['Roraima'] + list(base_rr['MUN_RES'].astype(str).unique())
        municipio_selecionado = st.selectbox("Selecione o Município", municipios)
    with col3:
        doencas = ['Todas'] + list(base_rr['NM_AGRAVO'].astype(str).unique())
        doenca_selecionada = st.selectbox("Selecione a Doença", doencas)

# Filtrar a base de dados de acordo com os filtros selecionados
base_filtrada = base_rr.copy()

if municipio_selecionado != 'Roraima':
    base_filtrada = base_filtrada[base_filtrada['MUN_RES'] == municipio_selecionado]

if doenca_selecionada != 'Todas':
    base_filtrada = base_filtrada[base_filtrada['NM_AGRAVO'] == doenca_selecionada]

# Gráfico de coluna
data_agrupada = base_filtrada.groupby('SEM_NOT').size().reset_index(name='counts')

if not data_agrupada.empty:
    fig_bar = px.bar(data_agrupada, x='SEM_NOT', y='counts', title=f"Notificações de {doenca_selecionada} em {ano_selecionado} no município de {municipio_selecionado}", text='counts')
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
    fig_bar.update_layout(xaxis_title="Semana Epidemiológica")
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("Não há dados disponíveis para o gráfico de colunas.")

# Gráfico de linhas para os últimos 5 anos com casos mensais
if not base_filtrada.empty:
    # Filtrar os dados para os últimos 5 anos
    anos_ultimos_5 = sorted(base_rr['NU_ANO'].unique())[-3:]
    base_filtrada_5_anos = base_rr[base_rr['NU_ANO'].isin(anos_ultimos_5)]

    # Agrupar os dados por semana epidemiológica (SEM_NOT) e ano (NU_ANO)
    data_agrupada = base_filtrada_5_anos.groupby(['SEM_NOT', 'NU_ANO']).size().reset_index(name='counts')

    # Gráfico de linhas para os últimos 5 anos com o total de notificações por semana
    fig_line = px.line(
        data_agrupada,
        x='SEM_NOT',
        y='counts',
        color='NU_ANO',  # Diferente cor para cada linha (ano)
        labels={'NU_ANO': 'Ano', 'SEM_NOT': 'Semana Epidemiológica', 'counts': 'Total de Notificações'},
        title="Total de Notificações por Semana Epidemiológica nos Últimos 5 Anos"
    )

    # Exibir o gráfico
    fig_line.update_traces(mode='lines+markers')  # Adicionar marcadores nas linhas para melhor visualização

    # Passar o use_container_width diretamente para o st.plotly_chart()
    st.plotly_chart(fig_line, use_container_width=True)



st.subheader(f"Dados Filtrados para {doenca_selecionada} no município de {municipio_selecionado}")
st.dataframe(base_filtrada)
