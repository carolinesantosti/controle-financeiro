import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard Financeiro da Carol",
    layout="wide"
)

st.title("💜 Dashboard Financeiro — Controle Inteligente de Gastos")

# Carregar dados
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("dados_processados.xlsx")
        return df
    except:
        return None

df = carregar_dados()

if df is None or df.empty:
    st.error("Nenhuma planilha encontrada. Gere o arquivo 'dados_processados.xlsx' primeiro.")
    st.stop()

# TOTAL GERAL
total = df["valor"].sum()
st.metric("Total Gasto no Período", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Agrupamento por categoria
df['categoria'] = df['categoria'].fillna("Outros")
categorias = df.groupby("categoria")["valor"].sum().sort_values(ascending=False)

# Gráfico 1 — Barras por categoria
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

# Gráfico 3 — Linha temporal
st.subheader("Gastos por Data")
df["data"] = pd.to_datetime(df["data"], dayfirst=True)

gastos_dia = df.groupby("data")["valor"].sum()

fig3, ax3 = plt.subplots()
gastos_dia.plot(kind="line", marker="o", ax=ax3)
ax3.set_ylabel("R$")
ax3.set_xlabel("Data")
st.pyplot(fig3)

# Gráfico 4 — Heatmap calendário (versão simples)
st.subheader("Mapa de Calor — Gastos por Dia do Mês")

df["dia"] = df["data"].dt.day
heat = df.groupby("dia")["valor"].sum()

fig4, ax4 = plt.subplots()
heat.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Dia do mês")
ax4.set_ylabel("R$")
st.pyplot(fig4)

st.divider()

st.subheader("📄 Detalhamento Completo")
st.dataframe(df)

