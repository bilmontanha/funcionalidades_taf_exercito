import streamlit as st
import app.funcoes as f

st.set_page_config(
     layout='wide',
     page_title='Funcionalidades TAF',
 )

st.markdown(f.config_pagina, unsafe_allow_html=True)

st.title("Bem-vindo ao Sistema TAF")
st.markdown("Selecione uma opção abaixo ou utilize o menu lateral:")

# Criando os "quadros clicáveis"
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown(
            """
            <div style='background-color: #0e1117; padding: 30px; border-radius: 10px; text-align: center;'>
                <h3 style='color:white;'>Conferência de Dados</h3>
                <p style='color:gray;'>Acesse a conferência de registros TAF</p>
                <a href='/Conferencia' target='_self'>
                    <button style='padding:10px 20px; font-size:16px;'>Acessar</button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

with col2:
    with st.container():
        st.markdown(
            """
            <div style='background-color: #0e1117; padding: 30px; border-radius: 10px; text-align: center;'>
                <h3 style='color:white;'>Dashboard</h3>
                <p style='color:gray;'>Visualize os resultados consolidados</p>
                <a href='/Dashboard' target='_self'>
                    <button style='padding:10px 20px; font-size:16px;'>Acessar</button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )