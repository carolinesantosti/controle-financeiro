import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard Financeiro da Carol",
    layout="wide"
)

st.title("💜 Dashboard Financeiro — Controle Inteligente de Gastos")

# ===============================
# 1) CARREGAR PLANILHA
# ===============================
@st.cache_data
def carregar_dados():
    try:
        arquivo = st.file_uploader("Envie o arquivo 'dados_processados.xlsx'", type=["xlsx"])

        if arquivo is None:
            st.warning("Nenhuma planilha encontrada. Envie o arquivo para continuar.")
            st.stop()

        df = pd.read_excel(arquivo)

        return df
    except Exception as e:
        st.error(f"Erro ao ler a planilha: {e}")
        return None


df = carregar_dados()

if df is None or df.empty:
    st.error("Nenhuma planilha válida foi carregada.")
    st.stop()

# ==========================================
# 2) REMOVER PAGAMENTO DA FATURA ANTERIOR
# ==========================================

# Se existir coluna de descrição, filtra por texto
if "descricao" in df.columns:
    df = df[~df["descricao"].str.contains("pagamento|fatura|pago", case=False, na=False)]

# Como fallback: remove valores absurdos que sempre são pagamento de fatura
df = df[df["valor"] < 4000]

# Remove valores nulos
df = df[df["valor"].notna()]

# ==========================================
# 3) TOTAL GERAL
# ==========================================
total = df["valor"].sum()
st.metric("Total Gasto no Período", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# ==========================================
# 4) AGRUPAMENTO
# ==========================================
df['categoria'] = df['categoria'].fillna("Outros")
categorias = df.groupby("categoria")["valor"].sum().sort_values(ascending=False)

# ==========================================
# 5) GRÁFICOS
# ==========================================

# -------- GRÁFICO 1 - Donut Chart --------
st.subheader("Distribuição Percentual por Categoria (Donut Chart)")

fig1, ax1 = plt.subplots(figsize=(6, 6))

wedges, texts, autotexts = ax1.pie(
    categorias,
    labels=categorias.index,
    autopct='%1.1f%%',
    pctdistance=0.85,
    textprops={'fontsize': 10}
)

# buraco no centro (donut)
centre_circle = plt.Circle((0, 0), 0.60, fc='white')
fig1.gca().add_artist(centre_circle)

ax1.axis('equal')
st.pyplot(fig1)

# -------- Gráfico 2 — Barras --------
st.subheader("Gastos por Categoria")
fig2, ax2 = plt.subplots(figsize=(10, 4))
categorias.plot(kind='bar', ax=ax2)
ax2.set_ylabel("R$")
ax2.set_xlabel("Categoria")
st.pyplot(fig2)

# -------- Gráfico 3 — Linha temporal --------
st.subheader("Gastos por Data")
df["data"] = pd.to_datetime(df["data"], dayfirst=True)

gastos_dia = df.groupby("data")["valor"].sum()

fig3, ax3 = plt.subplots(figsize=(10, 4))
gastos_dia.plot(kind="line", marker="o", ax=ax3)
ax3.set_ylabel("R$")
ax3.set_xlabel("Data")
st.pyplot(fig3)

# -------- Gráfico 4 — Mapa de Calor --------
st.subheader("Mapa de Calor — Gastos por Dia do Mês")

df["dia"] = df["data"].dt.day
heat = df.groupby("dia")["valor"].sum()

fig4, ax4 = plt.subplots(figsize=(10, 4))
heat.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Dia do mês")
ax4.set_ylabel("R$")
st.pyplot(fig4)

# ==========================================
# 6) TABELA FINAL
# ==========================================
st.divider()
st.subheader("📄 Detalhamento Completo")
st.dataframe(df)

