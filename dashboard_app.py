import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO

st.set_page_config(
    page_title="Dashboard Financeiro da Carol",
    layout="wide"
)

st.title("💜 Dashboard Financeiro — Controle Inteligente de Gastos")

# ================================
# CONFIGURAÇÃO DO GOOGLE DRIVE
# ================================
URL_PLANILHA = https://docs.google.com/spreadsheets/d/1aqYw6-t6HyGe-eOQXuR5bC3AQABT37cc/export?format=xlsx

@st.cache_data
def carregar_dados_drive():
    try:
        resposta = requests.get(URL_PLANILHA)
        resposta.raise_for_status()

        arquivo = BytesIO(resposta.content)
        df = pd.read_excel(arquivo)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar a planilha do Google Drive: {e}")
        return None

df = carregar_dados_drive()

if df is None or df.empty:
    st.error("Não foi possível carregar os dados da planilha.")
    st.stop()

# TOTAL GERAL
total = df["valor"].sum()
st.metric("Total Gasto no Período", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Categorias
df['categoria'] = df['categoria'].fillna("Outros")
categorias = df.groupby("categoria")["valor"].sum().sort_values(ascending=False)

# Gráfico 1 — Barras
st.subheader("Gastos por Categoria")
fig1, ax1 = plt.subplots()
categorias.plot(kind='bar', ax=ax1)
ax1.set_ylabel("R$")
ax1.set_xlabel("Categoria")
st.pyplot(fig1)

# Gráfico 2 — Pizza
st.subheader("Distribuição Percentual por Categoria")
fig2, ax2 = plt.subplots()
categorias.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# Gráfico 3 — Por dia
st.subheader("Gastos por Data")
df["data"] = pd.to_datetime(df["data"], dayfirst=True)
gastos_dia = df.groupby("data")["valor"].sum()

fig3, ax3 = plt.subplots()
gastos_dia.plot(kind="line", marker="o", ax=ax3)
ax3.set_ylabel("R$")
ax3.set_xlabel("Data")
st.pyplot(fig3)

# Gráfico 4 — Heatmap simples
st.subheader("Mapa de Calor — Gastos por Dia do Mês")
df["dia"] = df["data"].dt.day
heat = df.groupby("dia")["valor"].sum()

fig4, ax4 = plt.subplots()
heat.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Dia do mês")
ax4.set_ylabel("R$")
st.pyplot(fig4)

# Tabela completa
st.divider()
st.subheader("📄 Detalhamento Completo")
st.dataframe(df)


