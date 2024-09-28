import streamlit as st
import pandas as pd
import os
import time
from page0 import categoria
from page1 import cadastro_despesa
from page2 import minhas_despesas
from page3 import dashboards


def check_login_inputs(user):
    if not user or not passcode:
        return True
    if " " in user or " " in passcode:
        return True
    return False

def create_user(user,passcode):
    directory = os.getcwd()
    data_path = os.path.join(directory,"user_data")
    file_path = os.path.join(data_path,f"{user}_{passcode}.xlsx")
    category_path = os.path.join(data_path,f"{user}_{passcode}_category.xlsx")
    payment_path = os.path.join(data_path,f"{user}_{passcode}_payment.xlsx")
    df1 = pd.DataFrame({
        "DATA":[],
        "NOME DESPESA":[],
        "FORMA DE PAGAMENTO":[],
        "CATEGORIA":[],
        "VALOR":[],
    })
    df2 = pd.DataFrame({"CATEGORIAS":[]})
    df3 = pd.DataFrame({"FORMAS DE PAGAMENTO":[]})
    df1.to_excel(file_path,index=False)
    df2.to_excel(category_path,index=False)
    df3.to_excel(payment_path,index=False)
    return st.success("O seu usuário foi criado!\n\nVá para aba de login para realizá-lo.")


def check_user_not_exist(user,passcode):
    directory = os.getcwd()
    data_path = os.path.join(directory,"user_data")
    file_path = os.path.join(data_path,f"{user}_{passcode}.xlsx")
    if not os.path.exists(file_path):
        return True
    else:
        return False
    
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.write(os.getcwd())
    col1, col2, col3 = st.columns([1,5,1])
    aba_login_cadastro = st.sidebar.selectbox("Escolha uma opção:",options=["Login","Cadastro"])
    if aba_login_cadastro == "Login":
        with col2:
            col1, col2, col3 = st.columns([0.5,0.5,0.5])
            with col2:
                st.markdown("# LOGIN")
            with st.container(border=True):
                user = st.text_input("Usuário",placeholder="Digite o seu nome de usuário",help="O nome de usuário não deve conter espaços.")
                st.session_state.user = user
                passcode = st.text_input("Senha",placeholder="Insira sua senha",type="password",help="A senha não deve conter espaços.")
                st.session_state.passcode = passcode
                if st.button("Login",disabled=check_login_inputs(user)):
                    if check_user_not_exist(user=user,passcode=passcode):
                        st.warning("Nome de usuário e/ou senha incorreto.\n\nCaso ainda não possua uma conta vá para aba de cadastro.")
                    if not check_user_not_exist(user=user,passcode=passcode):
                        st.success("Você realizou o login!")
                        st.session_state.logged_in = True
                        st.rerun()
    else:
        col1,col2,col3 = st.columns([1,5,1])
        with col2:
            col1,col2,col3 = st.columns([0.5,1,0.5])
            with col2:
                st.markdown("# CADASTRO")
            with st.container(border=True):
                user = st.text_input("Usuário",placeholder="Digite o seu nome de usuário",help="O nome de usuário não deve conter espaços.")
                passcode = st.text_input("Senha",placeholder="Insira sua senha",type="password",help="A senha não deve conter espaços.")
                if st.button("Cadastrar",disabled=check_login_inputs(user)):
                    if check_user_not_exist(user=user,passcode=passcode):
                        create_user(user=user,passcode=passcode)
                    else:
                        st.warning("Usuário já existente, vá para aba de login.")
else:
    page = st.navigation([st.Page(categoria,title="Configurações de Despesas"),st.Page(cadastro_despesa,title="Cadastro de Despesa"),st.Page(minhas_despesas,title="Minhas Despesas"),st.Page(dashboards,title="Dashboard")])
    page.run()



