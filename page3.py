import streamlit as st
import pandas as pd
import os
import plotly.express as px

def dashboards():
    directory = os.getcwd()
    data_path = os.path.join(directory,"user_data")
    file_path = os.path.join(data_path,f"{st.session_state.user}_{st.session_state.passcode}.xlsx")
    payment_path = os.path.join(data_path,f"{st.session_state.user}_{st.session_state.passcode}_payment.xlsx")

    df_geral = pd.read_excel(file_path)
    df_payment = pd.read_excel(payment_path)

    if not df_geral.empty:
        col1,col2 = st.columns(2)
        with col1:
            month_unsorted = list(df_geral["DATA"].dt.month.value_counts().index)
            month_sorted = sorted(month_unsorted)
            month = st.selectbox("Selecione o mês:",month_sorted)
        with col2:
            year_unsorted = list(df_geral["DATA"].dt.year.value_counts().index)
            year_sorted = sorted(year_unsorted)
            year = st.selectbox("Selecione o ano:",year_sorted)

        df_show = df_geral[["DATA","NOME DESPESA","FORMA DE PAGAMENTO","CATEGORIA","VALOR"]]
        df_show = df_show[(df_show["DATA"].dt.month == month) & (df_show["DATA"].dt.year == year)]
        df_show["DATA"] = df_show["DATA"].dt.strftime("%d/%m/%Y")
        df_estilizado = df_show.style.format({
            "VALOR":"R$ {:.2f}"
        })

        st.markdown(
        """
        <style>
        body {
        font-family: 'Arial';
        }
        </style>
        """,
        unsafe_allow_html=True
        )

        st.divider()

        col1,col3 = st.columns([1,2])
        with col1:
            st.markdown(
                """
                <style>
                .valor_gasto {
                    text-align: center;
                    font-size: 30px;
                    font-weight: bold;
                }
                </style>
                <div style="text-align: center;">
                <div class="valor_gasto">
                VALOR TOTAL GASTO:
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            with st.container(border=True):
                st.markdown(
                    f"""
                <style>
                .valor_total {{
                    margin-bottom: 13px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 45px;
                }}
                </style>
                <div class="valor_total">
                R$ {df_show["VALOR"].sum()}
                </div>
                """,
                unsafe_allow_html=True
                )

        st.divider()

        col1,col2,col3 = st.columns([5,0.000001,5])

        with col1:
            with st.container(height=400,border=True):
                cores_roxo2 =  ['#8e06fc', '#9808fd', '#a109fd', '#ab0bfe']
                fig2 = px.pie(df_show, values=df_show["VALOR"],names=df_show["FORMA DE PAGAMENTO"],title="Gasto Por cartão",color_discrete_sequence=cores_roxo2)
                fig2.update_traces(textinfo="label",pull=[0.025,0.025,0.025,0.025],hovertemplate="Forma de Pagamento: %{label}<br>Valor Gasto: R$ %{value}<extra></extra>",texttemplate="<b>%{label}<b>",insidetextfont=dict(size=14))
                fig2.update_layout(
                    title={
                        "text":"GASTO POR CARTÃO",
                        "font":{
                            "size": 20,
                        },
                        "x":0.2
                    },
                )
                st.plotly_chart(fig2)

        with col3:
            with st.container(height=400,border=True):
                cores_roxo1 = ['#7000fa', '#7a02fb', '#8404fb', '#8e06fc', '#9808fd', '#a109fd', '#ab0bfe']
                fig1 = px.pie(df_show,values=df_show.groupby("CATEGORIA")["VALOR"].mean().round(2),names=df_show.groupby(["CATEGORIA"])[["VALOR"]].mean().index,title="Gasto Médio Unitário Por Categoria",color_discrete_sequence=cores_roxo1)
                fig1.update_traces(textinfo="label",pull=[0.05,0.05,0.05,0.05,0.05,0.05,0.05],hovertemplate="Categoria: %{label}<br>Média: R$ %{value}<extra></extra>",texttemplate="<b>%{label}<b>",insidetextfont=dict(size=12.5))
                fig1.update_layout(
                    title={
                        "text":"GASTO MÉDIO POR CATEGORIA",
                        "font":{
                            "size": 20,
                        },
                        "x":0.05
                    }
                )
                st.plotly_chart(fig1)
        st.write("")
        with st.container(border=True):
            fig = px.bar(df_show,x=df_show.groupby("CATEGORIA")["VALOR"].sum(),y=df_show.groupby("CATEGORIA")["VALOR"].sum().index,orientation="h",color_discrete_sequence=cores_roxo1,color=df_show.groupby("CATEGORIA")["VALOR"].sum().index,title="Gasto Por Categoria")
            fig.update_layout(
                    title={
                        "text":"GASTO POR CATEGORIA",
                        "font":{
                            "size": 20,
                        },
                        "x":0.35
                    },
                    showlegend=False,
                    xaxis_title="VALOR GASTO (R$)",
                    yaxis_title="CATEGORIA",
                    xaxis=dict(
                        title_font=dict(size=18, weight="bold"),
                        tickfont=dict(size=14,weight="bold")
                    ),
                    yaxis=dict(
                        title_font=dict(size=18, weight="bold"),
                        tickfont=dict(size=14,weight="bold")
                    )
                )
            fig.update_traces(hovertemplate="Categoria: %{y}<br>Total gasto: R$ %{x:.2f}<extra></extra>")
            st.plotly_chart(fig)
        


