import streamlit as st

#criando sistema de navegação (coloca no sidebar, também)
carregamento_page = st.Page('pages/Carregar_arquivo.py', title="Carregamento da planilha",icon=":material/upload_file:")
conferencia_page = st.Page('pages/Conferencia.py', title='Lançamentos com erro', icon=":material/error:")
dashboard_page = st.Page('pages/Dashboard.py', title="Dashboard", icon=":material/analytics:")
conferencia1_page = st.Page('pages/conferencia1.py', title='Lançar indices e verificar a menção final', icon=":material/check_box:")
baixar_page = st.Page('pages/Baixar_planilha_modelo.py', title='Baixar Planilha Modelo', icon=":material/download:")
#pg = st.navigation([home_page,conferencia_page,dashboard_page, baixar_page])
pg = st.navigation([carregamento_page,conferencia_page,dashboard_page, conferencia1_page, baixar_page])

st.set_page_config(
     layout='wide',
     page_title='Página de Carregamento',
 )

pg.run()

