import streamlit as st
import pandas as pd
import os
from datetime import datetime

def cadastro_despesa():
    
    def check_button(despesa,categoria,payment,value):
        if not despesa or not categoria or not payment or not value:
            st.warning("Preencha todos os campos!")
            return True
        else:
            return False


    
    directory = os.getcwd()
    data_path = os.path.join(directory,"user_data")
    file_path = os.path.join(data_path,f"{st.session_state.user}_{st.session_state.passcode}.xlsx")
    payment_path = os.path.join(data_path,f"{st.session_state.user}_{st.session_state.passcode}_payment.xlsx")
    categories_path = os.path.join(data_path,f"{st.session_state.user}_{st.session_state.passcode}_category.xlsx")

    df_geral = pd.read_excel(file_path)
    df_categories = pd.read_excel(categories_path)
    df_payment = pd.read_excel(payment_path)

    def cadastro(df,despesa,categoria,payment,value,data):
        df.loc[len(df)] = [data,despesa,payment,categoria,value]
        df["VALOR"] = df["VALOR"].round(2)
        df_geral["DATA"] = pd.to_datetime(df_geral["DATA"])
        df.to_excel(file_path,index=False)
        st.success(f"Você adicionou a despesa {despesa} com sucesso!")

    col1,col2,col3 = st.columns([2,10,1])
    with col2:
        st.markdown("# CADASTRO DE DESPESA")
    with st.container(border=True):
        co1,co2 = st.columns([2,1])
        with co1:
            despesa = st.text_input("Nome da Despesa:")
        with co2:
            date = st.text_input("Data:",value=datetime.today().strftime("%d/%m/%Y"))
        c1,c2,c3 = st.columns(3)
        with c1:
            categoria = st.selectbox("Categoria:",list(df_categories["CATEGORIAS"]))
        with c2:
            payment = st.selectbox("Forma de Pagamento:",df_payment["FORMAS DE PAGAMENTO"])
        with c3:
            value = st.number_input("Valor da Despesa:",placeholder="Ex. 100")
        with st.container():
            if st.button("Cadastrar",key="cadastro_despesa",use_container_width=True,disabled=check_button(despesa,categoria,payment,value)):
                cadastro(df=df_geral,despesa=despesa,payment=payment,categoria=categoria,value=value,data=date)
















