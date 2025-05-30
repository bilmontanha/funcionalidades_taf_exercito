import streamlit as st
import pandas as pd
from app.tabela_indice import *
import app.funcoes as f
    



# CSS personalizado para remover espaçamento e definir cor de fundo
st.markdown(f.config_pagina, unsafe_allow_html=True)

#pegando a tabela do session_state
if 'tabela' in st.session_state:
    tabela_tafs = st.session_state['tabela']
    #Pegando os taf existentes na planilha
    options = tabela_tafs['TAF'].value_counts().index.sort_values()
    selection = st.pills("Selecione o TAF", options, selection_mode="multi", default=None)
    nova_tabela = tabela_tafs[tabela_tafs['TAF'].isin(selection)]
    nova_tabela.reset_index(inplace=True, drop=True)

    #st.dataframe(nova_tabela)
    mencao_lancada = f.mencao_lancada(nova_tabela)
    lista_de_mencoes = f.lista_mencoes_pandas(nova_tabela)
    mencao_final = f.mencao_final(lista_de_mencoes)
    erros_lancamento = f.erros_lancamento(mencao_lancada=mencao_lancada, mencao_final=mencao_final)
    erros_lancamentos = pd.DataFrame(erros_lancamento.items(), columns=['Militar', 'Situação'])
    tabela_mencoes_indices = f.tabela_mencao_atividade(nova_tabela)

    col1, col2 = st.columns([0.3,0.7], vertical_alignment='top', border=True)
    with col1:
        opcoes_selectbox = ["Verificar erros de lançamento.", "Verificar meção geral e por atividade."]
        escolha = st.selectbox("Escolha uma opção abaixo",opcoes_selectbox, index=None)



    with col2:
        if escolha == 'Verificar erros de lançamento.':
            st.dataframe(erros_lancamentos)
            
        if escolha == "Verificar meção geral e por atividade.":
            st.dataframe(tabela_mencoes_indices)
else:
    st.markdown('# Carregue o arquivo na página de carregamento.')


        
        



#para teste
# diretorio_atual = Path.cwd()
# arquivo = diretorio_atual/'PLANILHA TAF(modelo).xlsx'
# uploaded_file = arquivo
# tabela_tafs = pega_excel(arquivo)
# selection = ['1º TAF']