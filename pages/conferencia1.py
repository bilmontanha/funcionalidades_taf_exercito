import streamlit as st
import pandas as pd
# import sys
# sys.path.append('..')
import app.funcoes as f
from app.tabela_indice import * 

def idade():
    idade = st.text_input('Informe a idade e pressione "Enter"')
    if idade:
        try:
            numero = int(idade)
            return numero
        except ValueError:
            st.error('Por favor, digite um número inteiro válido.')
    else:
        pass

def segmento():
    segmento = st.text_input('Informe o segmento: "M" para masculino ou "F" para feminino.').upper()
    if segmento:
            try: 
                if segmento != 'M' and segmento != 'F':
                    st.error('Por favor, digite "M" ou "F".')
                else:
                    return segmento 
            except ValueError:
                st.error('Por favor, digite "M" ou "F".')
    else:
        pass

def lem():
    lem = st.text_input('Informe a Linha de Ensino Militar: "B" para bélica ou "CT" para as demais.').upper()
    if lem:
            try: 
                if lem != 'B' and lem != 'CT':
                    st.error('Por favor, digite "B" ou "CT".')
                else:
                    return lem 
            except ValueError:
                st.error('Por favor, digite "B" ou "CT".')
    else:
        pass

def corrida():
    corrida = st.text_input('Informe a distância percorrida na corrida.')
    if corrida:
        try:
            corrida = int(corrida)
            return corrida
        except ValueError:
            st.error('Por favor, digite um número inteiro válido.')
    else:
        pass

def flexao():
    flexao = st.text_input('Informe a quantidade de flexões executadas.')
    if flexao:
        try:
            flexao = int(flexao)
            return flexao
        except ValueError:
            st.error('Por favor, digite um número inteiro válido.')
    else:
        pass

def abdominal():
    abdominal = st.text_input('Informe a quantidade de abdominais executados.')
    if abdominal:
        try:
            abdominal = int(abdominal)
            return abdominal
        except ValueError:
            st.error('Por favor, digite um número inteiro válido.')
    else:
        pass

def barra():
    barra = st.text_input('Informe a quantidade de barras executadas (No caso se segmento feminino da linha bélica acima de 40 anos, informar os segundos).')
    if barra:
        try:
            barra = int(barra)
            return barra
        except ValueError:
            st.error('Por favor, digite um número inteiro válido.')
    else:
        pass


dicionario = {'P/G': ['CEL'], 'NOME': ['Ciclano'], 'IDADE':[ 40], 'SEGMENTO':['M'], 'LEM':['B'], 'CORRIDA': [3000], 'FLEXÃO':[30], 'ABDOMINAL':[60], 'BARRA':['X'] }
tabela = pd.DataFrame(dicionario)
st.markdown('#### Insira os dados solicitados para a verificação da menção')

#pegando a idade
idade = idade()
tabela.at[0, 'IDADE'] = idade
if idade:
    segmento = segmento()
    tabela.at[0, 'SEGMENTO'] = segmento
    if segmento:
        lem = lem()
        tabela.at[0, 'LEM'] = lem
        if lem:
            corrida = corrida()
            tabela.at[0, 'CORRIDA'] = corrida
            m_corrida = f.determinar_mencao(idade, dicio_atividades, 'CORRIDA', lem, segmento, corrida)
            if corrida:
                st.write(f'Ficou com a menção "{m_corrida}" na corrida.')
                flexao = flexao()
                tabela.at[0, 'FLEXÃO'] = flexao
                m_flexao = f.determinar_mencao(idade, dicio_atividades, 'FLEXÃO', lem, segmento, flexao)
                if flexao:
                    st.write(f'Ficou com a menção "{m_flexao}" na flexão.')
                    abdominal = abdominal()
                    tabela.at[0, 'ABDOMINAL'] = abdominal
                    m_abdominal = f.determinar_mencao(idade, dicio_atividades, 'ABDOMINAL', lem, segmento, abdominal)
                    if abdominal:
                        st.write(f'Ficou com a menção "{m_abdominal}" no abdominal.')
                        if idade >= 50 or lem == 'CT':
                            barra = 'X'
                            resultado = f.lista_mencoes_pandas(tabela)
                            resultado_final = f.mencao_final(resultado)
                            st.success(f'ESSE MILITAR FICOU COM A MENÇÃO FINAL = "{resultado_final['CEL Ciclano']}"')
                        else:
                            barra = barra()
                            tabela.at[0, 'BARRA'] = barra
                            m_barra = f.determinar_mencao(idade, dicio_atividades, 'BARRA', lem, segmento, barra)
                            resultado = f.lista_mencoes_pandas(tabela)
                            resultado_final = f.mencao_final(resultado)
                            if barra:
                                st.write(f'Ficou com a menção "{m_barra}" na barra.')
                                st.success(f'ESSE MILITAR FICOU COM A MENÇÃO FINAL =  "{resultado_final['CEL Ciclano']}"')

