import streamlit as st
import pandas as pd
import os


def categoria():
    directory = os.getcwd()
    data_path = os.path.join(directory,"user_data")
    categories_path = os.path.join(data_path,f"{st.session_state.user}_{st.session_state.passcode}_category.xlsx")
    payment_path = os.path.join(data_path,f"{st.session_state.user}_{st.session_state.passcode}_payment.xlsx")

    df_categories = pd.read_excel(categories_path)
    df_payment = pd.read_excel(payment_path)
    
    categories = list(df_categories["CATEGORIAS"].value_counts().index)
    payment = list(df_payment["FORMAS DE PAGAMENTO"].value_counts().index)
    col1,col2,col3 = st.columns([0.5,1,0.5])

    with col2:
        st.markdown("# CONFIGURAÇÕES")
    ### ADICIONAR CAT OU PAY
    st.markdown("## ADICIONAR:")
    col1,col2 = st.columns(2)
    ### CATEGORIA
    with col1:
        
        with st.container(border=True):
            coluna1,coluna2,coluna3 = st.columns([3.5,10,3.5])
            with coluna2:
                st.markdown("## Categoria")
            category = st.text_input("Nome da categoria:")
            if st.button("Adicionar",key="categoria"):
                category_formatted = category.capitalize()
                if category_formatted in categories:
                    st.warning("Categoria já adicionada")
                else:
                    df_categories.loc[len(df_categories)] = category_formatted
                    df_categories.to_excel(categories_path,index=False)
                    st.success(f"A categoria {category} foi adicionada com sucesso!")


    ### PAGAMENTO
    with col2:
        
        with st.container(border=True):
            coluna1,coluna2,coluna3 = st.columns([0.5,1,0.5])
            with coluna2:
                st.markdown("## Cartões")
            payment_input = st.text_input("Nome da forma de pagamento:")
            if st.button("Adicionar",key="pagamento"):
                payment_formatted = payment_input.capitalize()
                if payment_input in payment:
                    st.warning("Forma de pagamento já adicionada")
                else:
                    df_payment.loc[len(df_payment)] = payment_formatted
                    df_payment.to_excel(payment_path,index=False)
                    st.success(f"A forma de pagamento {payment_input} foi adicionada com sucesso!")
    ### REMOVER CAT OU PAY
    st.write("")   
    st.markdown("## REMOVER:")
    ### CATEGORIA
    colums1,colums2 = st.columns(2)
    with colums1:
        with st.container(border=True,height=300):
            c1,c2,c3 = st.columns(3)
            with c2:
                st.markdown("CATEGORIA")
            st.table(df_categories)
        with st.container(border=True):
            number_category = st.number_input("Número da categoria a ser removida:",placeholder="Ex. 0",step=1)
            if st.button("Remover",key="R_categoria"):
                if number_category in list(df_categories.index):
                    st.success(f"A linha {number_category}, representando a categoria {list(df_categories.loc[number_category])[0]}, foi removida com sucesso!")
                    df_categories = df_categories.drop(number_category)
                    df_categories = df_categories.reset_index(drop=True)
                    df_categories.to_excel(categories_path,index=False)
                    
                else:
                    st.warning("A linha escolhida não consta na tabela.")
    ### PAYMENT
    with colums2:
        with st.container(border=True,height=300):
            co1,co2,co3 = st.columns([0.37,1,0.1])
            with co2:
                st.markdown("Forma de Pagamento")
            st.table(df_payment)
        with st.container(border=True):
            number_payment = st.number_input("Número da forma de pagamento a ser removida:",placeholder="Ex. 0",step=1)
            if st.button("Remover",key="R_payment"):
                if number_payment in list(df_payment.index):
                    st.success(f"A linha {number_payment}, representando a forma de pagamento {list(df_payment.loc[number_payment])[0]}, foi removida com sucesso!")
                    df_payment = df_payment.drop(number_payment)
                    df_payment = df_payment.reset_index(drop=True)
                    df_payment.to_excel(payment_path,index=False)
                else:
                    st.warning("A linha escolhida não consta na tabela")



            
            
