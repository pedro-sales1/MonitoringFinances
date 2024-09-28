import streamlit as st
import pandas as pd
import os

def minhas_despesas():
    directory = os.getcwd()
    data_path = os.path.join(directory,"user_data")
    file_path = os.path.join(data_path,f"{st.session_state.user}_{st.session_state.passcode}.xlsx")

    df_geral = pd.read_excel(file_path)
    
    
    if not df_geral.empty:
        col1,col2,col3 = st.columns(3)
        with col2:
            st.markdown("# DESPESAS")
        c1,c2 = st.columns(2)
        with c1:
            month_unsorted = list(df_geral["DATA"].dt.month.value_counts().index)
            month_sorted = sorted(month_unsorted)
            month = st.selectbox("Selecione o mês:",month_sorted)
        with c2:
            year_unsorted = list(df_geral["DATA"].dt.year.value_counts().index)
            year_sorted = sorted(year_unsorted)
            year = st.selectbox("Selecione o ano:",year_sorted)

        df_show = df_geral[["DATA","NOME DESPESA","FORMA DE PAGAMENTO","CATEGORIA","VALOR"]]
        df_show = df_show[(df_show["DATA"].dt.month == month) & (df_show["DATA"].dt.year == year)]
        df_show["DATA"] = df_show["DATA"].dt.strftime("%d/%m/%Y")
        df_estilizado = df_show.style.format({
            "VALOR":"R$ {:.2f}"
        })
        st.dataframe(df_estilizado,width=1000,height=450)
        with st.container(border=True):
            line = st.number_input("Insira a linha da despesa a ser removida:",step=1)
            with st.container():
                if st.button("Remover",use_container_width=True):
                    if line in list(df_geral.index):
                        st.success(f"Você removeu a linha {line}, representando a despesa {df_geral.loc[line]['NOME DESPESA']}")
                        df_geral = df_geral.drop(line)
                        df_geral = df_geral.reset_index(drop=True)
                        df_geral.to_excel(file_path,index=False)
    else:
        st.write("Adicione despesas para utilizar essa funcionalidade")






