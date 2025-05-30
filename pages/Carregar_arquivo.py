import streamlit as st
import app.funcoes as f
import pandas as pd


def pega_excel(arquivo):
    arquivo_excel = pd.ExcelFile(arquivo)#variável recebe todo o arquivo exel com suas abas
    dfs = [pd.read_excel(arquivo_excel,sheet_name=sheet).assign(TAF=sheet) for sheet in arquivo_excel.sheet_names] #cria uma lista com as abas da planilha
    tabela_tafs = pd.concat(dfs,ignore_index=True)#concatena as abas da planilha em uma só
    return tabela_tafs

st.markdown(f.config_pagina, unsafe_allow_html=True)

st.title("Bem-vindo ao aplicativo de conferência de TAF do 10º BIL Mth.")

if st.button("Vizualizar as Orientações para utilização do aplicativo", type='primary'):
    with st.container():
        st.markdown('''1) Esse aplicativo analisa um modelo prederteminado de tabela do Excel (.xlsx). Caso não tenha o modelo, clique no botão 'Baixar planilha modelo' ao lado.  
2) Não altere o nome das colunas e nem a estrutura da planilha.
3) A coluna 'SEGMENTO' deverá receber 'M' para masculino ou 'F' para feminino.
4) A coluna 'LEM' deverá receber 'B' para LEMB ou 'CT' para LEMS,LEMC ou LEMCT.
5) Antes de carregar a planilha, verifique se está toda preenchida.
6) A coluna 'OBS' terá lançamento livre para fins de controle interno.
7) Nas atividades não realizadas pelos militares que fazem TAF Alternativo deverá ser lançado 'A', para evitar erros.
8) Militares que não realizaram o TAF deverão receber 'NR' no lugar dos índices e da menção.
9) Militares das outras LEM, que não a bélica, ou com 50 anos ou mais, devem receber 'X' no lugar do índice da barra.
10) Sugestões de melhoria: carlos.2cmf@gmail.com
    ''')
st.markdown("##### CARREGUE A PLANILHA A SER ANALISADA, CLICANDO NO BOTÃO ABAIXO.")
uploaded_file = st.file_uploader("Carregue o arquivo", label_visibility='hidden')
if uploaded_file is not None:
    tabela_tafs = pega_excel(uploaded_file)#carrega a tabela para um dataframe
    tabela_tafs.reset_index(inplace=True, drop=True)
    #jogando a tabela para o state para ser utilizadas nas outras páginas
    if 'tabela' not in st.session_state:
        st.session_state["tabela"] = tabela_tafs
    # Criando os "quadros clicáveis"
    col1, col2 = st.columns(2, vertical_alignment='center')

    st.markdown("#### Selecione uma opção abaixo ou utilize o menu lateral:")
    with col1:
        st.markdown(
            """
            <div style='background-color: #0e1117; padding: 30px; border-radius: 10px; text-align: center;'>
                <h3 style='color:white;'>Conferência de Dados</h3>
                <p style='color:gray;'>Verifique os erros de lançamento na planilha</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Acessar Conferência"):
            st.switch_page("pages/Conferencia.py")
    with col2:
        st.markdown(
            """
            <div style='background-color: #0e1117; padding: 30px; border-radius: 10px; text-align: center;'>
                <h3 style='color:white;'>Dashboard</h3>
                <p style='color:gray;'>Visualize os resultados consolidados</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Acessar Dashboard"):
            st.switch_page("pages/Dashboard.py")
else: 
    pass
    #st.write("")