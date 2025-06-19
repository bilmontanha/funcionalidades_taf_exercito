import streamlit as st
import app.funcoes as f
import plotly.express as px
from app.tabela_indice import *


######### INICIANDO A CRIAÇÃO DA PÁGINA

# CSS personalizado para remover espaçamento e definir cor de fundo
#st.markdown(f.config_pagina, unsafe_allow_html=True) desabilitado por dificultar a vizualização em celular

#Puxando a tabela do state
if 'tabela' in st.session_state:
    tabela_tafs = st.session_state["tabela"]


    #TÍTULO
    st.markdown("<h2 style='text-align: center;'>Gráficos do TAF</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.3,0.7], vertical_alignment='top', border=True)
    #Montando o menu da esqueda (filtros em sequência)
    with col1:
        st.markdown("#### :material/filter_alt: FILTROS ")
        #Coletando as opções na coluna do TAF
        op_taf = tabela_tafs["TAF"].unique()
        #Botões e filtros para o TAF
        with st.container(border=True):
            taf_selecionados = st.pills("# Selecione o TAF", op_taf, selection_mode="multi")
            if taf_selecionados:
                tabela_final = tabela_tafs[tabela_tafs['TAF'].isin(taf_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)
            else:
                tabela_final = tabela_tafs.copy()
        
        #coletando as opções de segmento
        op_seg = tabela_final["SEGMENTO"].unique()
        #Filtro para segmento
        with st.container(border=True):
            seg_selecionados = st.pills("Selecione o Segmento", op_seg, selection_mode="multi")
            if seg_selecionados:
                tabela_final = tabela_final[tabela_final['SEGMENTO'].isin(seg_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)
        
        #coletando as opções de posto e graduação
        op_pg = tabela_final["P/G"].unique()
        #Filtro Posto e Graduação
        with st.container(border=True):
            pg_selecionados = st.pills("Selecione o Posto/Graduação", op_pg, selection_mode="multi")
            if pg_selecionados:
                tabela_final = tabela_final[tabela_final['P/G'].isin(pg_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)
        
        #Coletando as opções de subunidade
        op_su = tabela_final["COMPANHIA"].unique()
        #Filtro Posto e Graduação
        with st.container(border=True):
            su_selecionados = st.pills("Selecione a Companhia/Fração", op_su, selection_mode="multi")
            if su_selecionados:
                tabela_final = tabela_final[tabela_final['COMPANHIA'].isin(su_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)
        
        #coletando as opções de chamada
        op_ch = tabela_final["CHAMADA"].unique()
        #Filtro Chamadas
        with st.container(border=True):
            ch_selecionados = st.pills("Selecione a Chamada", op_ch, selection_mode="multi")
            if ch_selecionados:
                tabela_final = tabela_final[tabela_final['CHAMADA'].isin(ch_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)


    #CRIA UMA TABELA COM AS MENÇÕES POR ATIVIDADE
    tabela_men_atv = f.tabela_mencao_atividade(tabela_final)


    
        #Montando a coluna dos gráficos
    with col2:
        if taf_selecionados:
            #se mais de um taf for selecionado
            if len(taf_selecionados) >= 2:
                f.graf_linhas_mencoes_por_taf(tabela_final)
            
            #se só um taf for selecionado
            else:
                #coletando as opções de atividade e menção
                op_atv = tabela_tafs.columns[5:10]
                atv_selecionados = st.pills("Selecione a opção para combinação dos gráficos", op_atv, selection_mode="multi")
                #devolvendo boleanos para as variaveis corrida, flexão, abdominal, barra e mencao para poder utilizar nas funções de gráficos
                corrida, flexao, abdominal, barra, mencao = f.devolve_boleanos(atv_selecionados)
                atividades = (corrida, flexao, abdominal, barra, mencao)
    
                # só menção
                if (False, False, False, False, True) == atividades:
                    st.markdown("#### Gráfico da menção final")
                    st.pyplot(f.grafico_pizza(tabela_final, 'MENÇÃO'))
                
                #só corrida
                elif (True, False, False, False, False) == atividades:
                    f.idade_seg_atv(tabela_final, 'CORRIDA')
                    st.write('MENÇÕES POR ATIVIDADE - CORRIDA')
                    tabela = f.tabela_mencao_atividade_limpa(tabela_men_atv,'M_CORRIDA')
                    st.pyplot(f.grafico_pizza(tabela, 'M_CORRIDA'))
                
                #só flexão
                elif (False, True, False, False, False) == atividades:
                    f.idade_seg_atv(tabela_final, 'FLEXÃO')
                    st.write('MENÇÕES POR ATIVIDADE - FLEXÃO')
                    tabela = f.tabela_mencao_atividade_limpa(tabela_men_atv,'M_FLEXÃO')
                    st.pyplot(f.grafico_pizza(tabela, 'M_FLEXÃO'))
                
                # só abdominal            
                elif (False, False, True, False, False) == atividades:
                    f.idade_seg_atv(tabela_final, 'ABDOMINAL')
                    st.write('MENÇÕES POR ATIVIDADE - ABDOMINAL')
                    tabela = f.tabela_mencao_atividade_limpa(tabela_men_atv,'M_ABDOMINAL')
                    st.pyplot(f.grafico_pizza(tabela, 'M_ABDOMINAL'))
                
                # só barra
                elif (False, False, False, True, False) == atividades:
                    f.idade_seg_atv(tabela_final, 'BARRA')
                    st.write('MENÇÕES POR ATIVIDADE - BARRA')
                    tabela = f.tabela_mencao_atividade_limpa(tabela_men_atv,'M_BARRA')
                    st.pyplot(f.grafico_pizza(tabela, 'M_BARRA'))

                # nenhuma opção marcada
                elif (False, False, False, False, False) == atividades:
                    st.write("Escolha uma ou mais opções.")
                else:
                    st.plotly_chart(f.grafico_linha(tabela=tabela_men_atv, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
        else:
            st.markdown("#### Escolha  um ou mais TAF na barra lateral esquerda.")    
        
    #Mostrar tabela no final
    if st.button('MOSTRAR TABELA FILTRADA'): #,on_click=None):
        tabela_final
else:
    st.markdown('# Carregue o arquivo na página de carregamento.')
    st.page_link("pages/Carregar_arquivo.py", label="Página de Carregamento", icon=":material/upload_file:")




