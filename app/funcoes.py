
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
from app.tabela_indice import *


def determinar_mencao(idade,dicio_atividades,atividade,lem,segmento,indice):# retorna a menção correta para o índice indicado
    '''segmento - retirado da coluna 'SEGMENTO' da tabela
       idade - retirado da coluna "IDADE" da tabela
       atividade - nome da coluna da atividade na tabela
       indice - item retirado da coluna da atividade
       lem - retirado da coluna "LEM"
    '''
    #verificação de erro na coluna IDADE
    if idade == None or isinstance(idade,str) or idade < 18 or str(idade) == 'nan':
        return 'erro idade'

    #verificação de erro na coluna SEGMENTO
    if segmento not in ['M','F'] or segmento == None or str(segmento) == 'nan':
        return 'erro no segmento'

    #verificação de erro na coluna LEM
    if lem not in ['B','CT'] or lem == None or str(lem) == 'nan':
        return 'erro na LEM'
    
    #verificação de erro no lançamento dos índices
    teste_indice = str(indice) #caso esteja vazio, torna o espaço vago em na string 'nan'.
    #Caso seja atividade de barra, já adianta 'X' para CT e B > 50
    if atividade == 'BARRA':
        if lem == 'CT':
            return 'X'
        if lem == 'B':
            if idade < 50:
                if teste_indice == 'None' or teste_indice == 'nan':
                    return 'NR'
            else:
                return 'X'
    # Caso não seja BARRA e esteja vazio
    if teste_indice == 'None' or teste_indice == 'nan':
        return 'NR'
    # Caso não seja barra e possua uma string lançada
    if isinstance(indice,str):
        if indice == 'NR' or indice == 'A':
            return indice
        else:
            return 'NR'


# determinar a faixa de idade
    if lem == 'B':
            for faixa in dicio_atividades[lem][atividade][segmento].keys():
                inicio, fim = map(int, faixa.split('-'))
                if inicio <= idade <= fim:
                    faixa = faixa
                    break
    else:
        if atividade == 'BARRA':
            faixa = 'X'
        else:
            for faixa in dicio_atividades[lem][atividade][segmento].keys():
                inicio, fim = map(int, faixa.split('-'))
                if inicio <= idade <= fim:
                    faixa = faixa
                    break

#determinar a menção
    if faixa != 'X':
        for f in dicio_atividades[lem][atividade][segmento].keys():
            if f == faixa:
                dicio_mencoes = dicio_atividades[lem][atividade][segmento][f]
                if isinstance(dicio_mencoes, dict):
                    for k, (min,max) in dicio_mencoes.items():
                        if min <= indice <= max:
                            return k
                else:
                    if dicio_mencoes == 0:
                        return "S"
                    if indice >= dicio_mencoes:
                        return "S"
                    if indice < dicio_mencoes:
                        return "I"
    else:
        return indice

    

#criar colunas com as menções de cada índice.
def tabela_mencao_atividade(tabela): 
    #try:
        copia_tabela = tabela.copy(deep=True)
        atividades = ['CORRIDA', 'FLEXÃO', 'ABDOMINAL', 'BARRA']
        for atividade in atividades:
            copia_tabela[f"M_{atividade}"] = copia_tabela.apply(lambda row: determinar_mencao(row['IDADE'],dicio_atividades,atividade, row['LEM'], row['SEGMENTO'], row[atividade]), axis=1)
        nova_tabela = copia_tabela[(['P/G', 'NOME','M_CORRIDA','M_FLEXÃO','M_ABDOMINAL','M_BARRA','MENÇÃO','TAF'])]
        return nova_tabela
    #except Exception as e:
        #return print(e)

def tabela_mencao_atividade_limpa(tabela,atividade):
    copia_tabela = tabela.copy(deep=True)
    copia_tabela = copia_tabela[[atividade]]
    copia_tabela = copia_tabela[~((copia_tabela[atividade] == 'NR') | (copia_tabela[atividade] == 'X') | (copia_tabela[atividade] == 'A') | (copia_tabela[atividade].isna()) | (copia_tabela[atividade].str.contains('erro', case=False, na=False)))]
    return copia_tabela

##Devolvendo Boleanos para os variáveis corrida, flexão, abdominal, barra e menção
def devolve_boleanos(lista):
    if 'CORRIDA' in lista:
        corrida = True
    else:
        corrida = False
    if 'FLEXÃO' in lista:
        flexao = True
    else:
        flexao = False
    if 'ABDOMINAL' in lista:
        abdominal = True
    else:
        abdominal = False
    if 'BARRA' in lista:
        barra = True
    else:
        barra = False
    if 'MENÇÃO' in lista:
        mencao = True
    else:
        mencao = False
    return corrida, flexao, abdominal, barra, mencao


########################## FUNÇÕES PARA O ARQUIVO analise_taf.py#############################

#devolve um int com o número de linhas da tabela
def pega_nr_linhas(tabela):
    try:
        return tabela.index.stop
    except:
        return int(tabela.index[-1])


def lista_mencoes_pandas(tabela):
    dicionario = dict()
    linhas = pega_nr_linhas(tabela)
    for l in range(0, linhas):#retirei o '+1' que estava somando com a variavel 'lista' verificar se extá excluindo a última linha
        lista = list()
        #pega os indices
        idade = tabela.iloc[l]['IDADE']
        segmento = tabela.iloc[l]['SEGMENTO']
        lem = tabela.iloc[l]['LEM']
        corrida = tabela.iloc[l]['CORRIDA']
        flexao = tabela.iloc[l]['FLEXÃO']
        abdominal = tabela.iloc[l]['ABDOMINAL']
        barra = tabela.iloc[l]['BARRA']
        #pega as menções
        lista.append(determinar_mencao(idade, dicio_atividades, 'CORRIDA', lem, segmento, corrida))
        lista.append(determinar_mencao(idade, dicio_atividades, 'FLEXÃO', lem, segmento, flexao))
        lista.append(determinar_mencao(idade, dicio_atividades, 'ABDOMINAL', lem, segmento, abdominal))
        lista.append(determinar_mencao(idade, dicio_atividades, 'BARRA', lem, segmento, barra))
        dicionario[f'{tabela.iloc[l]['P/G']} {tabela.iloc[l]['NOME']}'] = lista
    return dicionario



#função para verificar o dicionário limpo e informar qual é a menção final do militar
#Essa função ainda vai exibir os militares com erro
def mencao_final(dicio):
    dicio_copia = dicio.copy()#só para não alterar o dicionário original
    resultado = dict()
    for k, v in dicio_copia.items():
        if v.count('NR') >= 4:
            resultado[k] = 'TAF não realizado'
            continue
        if 'erro no segmento' in v:
            resultado[k] = 'erro no segmento'
            continue
        if 'erro na LEM' in v:
            resultado[k] = 'erro na LEM'
            continue
        if 'erro idade' in v:
            resultado[k] = 'erro idade'
            continue
        if 'NR' in v[0]:
            resultado[k] = 'Faltando o índice da CORRIDA'
            continue
        if 'NR' in v[1]:
            resultado[k] = 'Faltando o índice da FLEXÃO'
            continue
        if 'NR' in v[2]:
            resultado[k] = 'Faltando o índice do ABDOMINAL'
            continue
        if 'NR' in v[3]:
            resultado[k] = 'Faltando o índice da BARRA'
            continue
        if 'A' in v:
            if 'I' in v:
                resultado[k] = 'I'
                continue
            else:
                resultado[k] = 'R'
                continue
        if 'I' in v:
            resultado[k] = 'I'
            continue
        if 'R' in v:
            resultado[k] = 'R'
            continue
        if 'B' in v:
            resultado[k] = 'B'
            continue
        if 'MB' in v:
            resultado[k] = 'MB'
            continue
        if 'E' in v:
            resultado[k] = 'E'
            continue
        if 'S' in v:
            resultado[k] = 'S'
    return resultado



def mencao_lancada(tabela):#pega as menções que foram lançadas na coluna  'MENÇÃO'
    dicionario = dict()
    linhas = pega_nr_linhas(tabela)
    for l in range(0, linhas):
        pg_nome = f'{tabela.iloc[l]['P/G']} {tabela.iloc[l]['NOME']}'
        mencao = tabela.iloc[l]['MENÇÃO']
        dicionario[pg_nome] = mencao
    return dicionario

#compara a menção lançada com a que teria que ser
def erros_lancamento(mencao_lancada, mencao_final):
    mencao_lancada_copia = mencao_lancada.copy()
    mencao_final_copia = mencao_final.copy()
    dicionario = dict()
    for k,v in mencao_lancada_copia.items():
        #try:
        if mencao_final_copia[k] != v:
            if mencao_final_copia[k] == 'TAF não realizado':
                continue
            elif mencao_final_copia[k] == 'erro no segmento':
                dicionario[k] = 'Existe um erro no lançamento da coluna "SEGMENTO". Dado ausente ou lançado errado (só aceita "M" ou "F")'
            elif mencao_final_copia[k] == 'erro na LEM':
                dicionario[k] = 'Existe um erro no lançamento da coluna "LEM". Dado ausente ou lançado errado (só aceita "B" ou "CT")'
            elif mencao_final_copia[k] == 'erro idade':
                dicionario[k] = 'Existe um erro no lançamento da coluna "IDADE". Dado ausente ou lançado errado (só aceita números inteiros)'
            elif mencao_final_copia[k] == 'Faltando o índice da CORRIDA':
                dicionario[k] = 'Faltando o índice da CORRIDA'
            elif mencao_final_copia[k] == 'Faltando o índice da FLEXÃO':
                dicionario[k] = 'Faltando o índice da FLEXÃO'
            elif mencao_final_copia[k] == 'Faltando o índice do ABDOMINAL':
                dicionario[k] = 'Faltando o índice do ABDOMINAL'
            elif mencao_final_copia[k] == 'Faltando o índice da BARRA':
                dicionario[k] = 'Faltando o índice da BARRA'
            #verifica se o a menção está sem lançamento
            elif str(v) == 'nan':
                dicionario[k] = f'Não foi lançada menção para o militar. A menção correta a ser lançada é: {mencao_final_copia[k]}'
            else:        
                dicionario[k] = f'Consta com a menção {v}, mas o correto é a menção/lançamento: {mencao_final_copia[k]}'
        # except Exception as e:
        #     return f'Erro: {e}'
    return dicionario





####################-> GRÁFICOS <-#####################

#Gráfico Pizza para as menções
#criando um dicionário de cores para manter a cor fixa para cada menção no gráfico pizza
color_dict = {
    'E': 'Turquoise',
    'MB': 'orange',
    'B': 'green',
    'R': 'brown',
    'I': 'Coral',
    'NR': 'Silver',
    'S': 'Violet'
}
#Função para gráfico pizza
def grafico_pizza(tabela, info):
    try:
        info_tab = tabela[info].value_counts()
        labels,sizes = list(),list()
        for k, v in info_tab.items():
            labels.append(k)
            sizes.append(v)
        colors = [color_dict[label] for label in labels]#cria o dicinário para cada cor no labels levantado utilizando o dicionário color_dict
        pizza, ax = plt.subplots() #primeira variável é figura
        #pizza_oficiais.set_facecolor(color='black') #coloca o fundo preto
        #for text in ax.texts: # para colocar a letras na cor branca
            #text.set_color('white')#colocando as letras na cor branca
        ax.pie(
            sizes, #quantidade das menções
            labels=labels,# identificação das menções
            colors=colors,# le o dicionario com as cores pré-definidas
            autopct='%1.1f%%', #para aparecer as porcentagens
            wedgeprops={'width':0.4},# Cria um buraco no fundo do gráfico, fazendo virar um anel
            pctdistance=0.8, #centraliza as porcentagens
            textprops={'fontsize':12, 'weight':'bold'},
            )
        ax.axis('equal')#deixa o gráfico no formato redondo
        ax.text(0,0, info, ha='center', va='center', fontsize=16, color='black')#coloca o título do gráfico no centro (dois primeiros números dizem respeito a posição)
        return pizza
    except Exception as e:
        return st.exception(e)





###### Gráfico de barra para representar a quantidade de militares na quantidade do indice alcançado na atividade
def para_um(tabela, atividade):
    tabela = tabela[~((tabela[atividade] == 'A') | (tabela[atividade].isna()) | (tabela[atividade] == 'X') | (tabela[atividade] == 'NR'))]# trata a tabela para tirar "A", nulo, 'NR' e 'X'
    df_mencao_count = tabela[atividade].value_counts().reset_index()
    df_mencao_count.columns = [atividade, "count"]
    fig_bar_mencao = px.bar(
    df_mencao_count, 
    x= atividade, 
    y="count", 
    title=f"Quantidade de Militares X Quantidade de {atividade}",
    labels={atividade: f'Quantidade de {atividade}', "count": "Quantidade de Militares"}
    )
    st.plotly_chart(fig_bar_mencao)

####Gráfico de disperção para uma atividade, levando em consideração a idade e o segmento
def idade_seg_atv(tabela, atividade):
    tabela = tabela[~((tabela[atividade] == 'A') | (tabela[atividade].isna()) | (tabela[atividade] == 'X') | (tabela[atividade] == 'NR'))] # trata a tabela para tirar "A", nulo e 'X'
    try:
        cores_personalizadas = ['#377eb8','#e41a1c']
        media_atividade = tabela[atividade].mean()
        fig_scatter = px.scatter(tabela, 
                                x="IDADE", 
                                y= atividade,
                                color="SEGMENTO",
                                color_discrete_sequence=cores_personalizadas,
                                hover_data=["NOME", "P/G"],
                                title=f"Desempenho na(o) {atividade} por SEGMENTO E IDADE")
        fig_scatter.add_hline(
        y=media_atividade,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Média: {media_atividade:.2f}",
        annotation_position="top right"
    )
        st.plotly_chart(fig_scatter)
    except:
        st.write(f"Ocorreu um erro, provavelmente a coluna {atividade} está com algum valor lançado errado. Clique no botão 'Mostrar Tabela Filtrada' e tente identificar e corrigir.")





#Gráfico para comparar a evolução dos TAF
def graf_linhas_mencoes_por_taf(df):
    """
    Linha das menções (I, R, B, MB, E) para 1º, 2º e 3º TAF.
    df precisa ter colunas 'TAF' e 'MENÇÃO'.
    """
    df = df[~((df['MENÇÃO'] == 'A') | (df['MENÇÃO'].isna()) | (df['MENÇÃO'] == 'X') | (df['MENÇÃO'] == 'NR'))]
    
    ordem = ['I', 'R', 'B', 'MB', 'E']

    # 1. Conta menções por TAF
    cont = (df[df['MENÇÃO'].isin(ordem)]
            .groupby(['TAF', 'MENÇÃO'])
            .size()
            .reset_index(name='quantidade'))

    # 2. Garante ordem no eixo X
    cont['MENÇÃO'] = pd.Categorical(cont['MENÇÃO'],
                                    categories=ordem,
                                    ordered=True)

    # 3. Gráfico
    fig = px.line(
        cont.sort_values('MENÇÃO'),
        x='MENÇÃO',
        y='quantidade',
        color='TAF',
        markers=True,
        category_orders={'MENÇÃO': ordem},
        title='Evolução das Menções por TAF'
    )
    fig.update_layout(xaxis_title='Menção',
                      yaxis_title='Quantidade',
                      legend_title_text='TAF')
    return st.plotly_chart(fig)




#GRÁFICO LINHA PARA COMPARAR MENÇÕES DAS ATIVIDADES
def grafico_linha(tabela, **kwargs):
    '''Chaves válidas para o **kwargs:
    corrida= , flexao=, abdominal=, barra= e mencao= 
    as chaves deverão ter valor boleano'''
    cores_fixas = {
    "Menção Geral": "black",
    "Corrida":   "red",
    "Flexão":    "orange",
    "Abdominal": "green",
    "Barra":     "pink",
}
    
    atividades = dict()
    for k,v in kwargs.items():
        if v:
            if k == 'flexao': #só para não mudar o nome da variável e dar erro em outra parte do código.
                atividades['Flexão'] = 'M_FLEXÃO'
            elif k == 'mencao':
                atividades['Menção Geral'] = 'MENÇÃO'
            else:
                atividades[k.capitalize()] = f'M_{k.upper()}'
        
# ── 3. Conta quantas menções por atividade ───────────────────────────
    ordem = ["I", "R", "B", "MB", "E"]       # sequência fixa no eixo X
    ordem_atividades = ['Menção Geral', 'Corrida', 'Flexão', 'Abdominal', 'Barra']
    registros = []

    for nome, coluna in atividades.items():
        cont = tabela[coluna].value_counts()
        for mencao in ordem:
            registros.append(
                {"Atividade": nome,
                "Menção": mencao,
                "Quantidade": int(cont.get(mencao, 0))}
            )

    long_df = pd.DataFrame(registros)
    long_df["Menção"] = pd.Categorical(long_df["Menção"], categories=ordem, ordered=True)

    # ── 4. Gráfico de linhas ─────────────────────────────────────────────
    fig = px.line(
        long_df.sort_values("Menção"),
        x="Menção",
        y="Quantidade",
        color="Atividade",
        markers=True,                        # pontinhos em cada menção
        title="Distribuição das Menções por Atividade",
        category_orders={
            "Menção": ordem,
            'Atividade':ordem_atividades},
        color_discrete_map=cores_fixas
    )
    fig.update_layout(
        yaxis_title="Quantidade de Menções",
        legend_title_text="Atividade",
    )

    # Se estiver num script Streamlit:
    return fig

####CONFIGURAÇÃOS DA PÁGINA
config_pagina = """
<style>
    /* Remover espaçamento superior e ocultar elementos do Streamlit */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        margin-top: 0rem;
    }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Definir cor de fundo da página inteira */
    .stApp {
        background-color: #e6ffee;  /* Verde */
    }
    
    /* Definir cor de fundo para os componentes */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: #4b5320;
        border: 2px solid #ddd;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    
    /* Estilo para a tabela de dados */
    div.stDataFrame {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Estilizando os botões de pílulas */
    .stPills {
        background-color: #ffffff;
    }
</style>
"""











############################somente para realização de testes##########################
#######################################################################################
if __name__=='__main__':
    from pathlib import Path
    from tabela_indice import *
    from pprint import pprint
    import pandas as pd
    #diretorio_atual = Path.cwd()
    arquivo = 'C:/Users/SCmt/Desktop/python/funcionalidades_taf_exercito/pages/PLANILHA TAF(modelo).xlsx'
    arquivo_casa = 'C:/Users/carlo/Desktop/python/funcionalidades_taf_exercito/pages/PLANILHA TAF(modelo).xlsx'
    arquivo_excel = pd.ExcelFile(arquivo_casa)#variável recebe todo o arquivo exel com suas abas
    dfs = [pd.read_excel(arquivo_excel,sheet_name=sheet).assign(TAF=sheet) for sheet in arquivo_excel.sheet_names] #cria uma lista com as abas da planilha
    tabela_tafs = pd.concat(dfs,ignore_index=True)#concatena as abas da planilha em uma só

    #tabela_tafs = tabela_tafs[~((tabela_tafs["CORRIDA"] == 'A') | (tabela_tafs["CORRIDA"].isna()) | (tabela_tafs["CORRIDA"] == 'X'))] # trata a tabela para tirar "A", nulo e 'X'
    #tabela_tafs["menção item"] = tabela_tafs.apply(lambda row: determinar_mencao(row['IDADE'],dicio_atividades,'CORRIDA', row['LEM'], row['SEGMENTO'], row['CORRIDA']), axis=1)
    #idade,dicio_atividades,atividade,lem,segmento,indice
   
    tabela_testes = tabela_tafs[tabela_tafs['TAF'].isin(['1º TAF 2024'])]
    nova_tabela = tabela_mencao_atividade(tabela_tafs)
    #nova_tabela.to_excel('tabela.xlsx', index=False)


    t = nova_tabela[['M_BARRA']]
    t.value_counts()
    tabela_tafs.value_counts().index

    nt = tabela_mencao_atividade_limpa(nova_tabela,'M_FLEXÃO')
    nt.value_counts()
    taf = ['1º TAF', '2º TAF']
    tabela1 = tabela_mencao_atividade(tabela_testes)
    pprint(tabela1)
    tabela2 = lista_mencoes_pandas(tabela_tafs)
    #tabela1.to_excel('teste.xlsx')
    mencao_final1 = mencao_final(tabela2)
    mencoes_lancadas = mencao_lancada(tabela_tafs)

    erros = erros_lancamento(mencoes_lancadas, mencao_final1)
    a = 'X'
    b = str(a)




