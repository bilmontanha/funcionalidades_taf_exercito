import streamlit as st


st.set_page_config(
     layout='wide',
     page_title='Dash TAF - 10º BIL Mth',
 )

with open('pages/PLANILHA TAF(modelo).xlsx', 'rb') as file:
    arquivo_excel = file.read()

st.markdown("### Ainda não tem a planilha modelo? Faça o download no botão abaixo.")
st.download_button(
    label="# Baixar a planilha modelo",
    data=arquivo_excel,
    file_name='PLANILHA TAF.xlsx',
    mime = 	'application/vnd.ms-excel',
    icon= ':material/download:',
    type= 'primary'
        )