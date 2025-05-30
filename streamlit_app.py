import streamlit as st

#criando sistema de navegação (coloca no sidebar, também)
carregamento_page = st.Page('pages/Carregar_arquivo.py', title="Carregamento da planilha")
conferencia_page = st.Page('pages/Conferencia.py', title='Verificação de erros de lançamento')
dashboard_page = st.Page('pages/Dashboard.py', title="Dashboard")
baixar_page = st.Page('pages/Baixar_planilha_modelo.py', title='Baixar Planilha Modelo')
#pg = st.navigation([home_page,conferencia_page,dashboard_page, baixar_page])
pg = st.navigation([carregamento_page,conferencia_page,dashboard_page, baixar_page])

st.set_page_config(
     layout='wide',
     page_title='Página de Carregamento',
 )

pg.run()


