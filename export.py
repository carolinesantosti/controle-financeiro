# export.py
import pandas as pd
import matplotlib.pyplot as plt

def gerar_excel(df, output="dados_processados.xlsx"):
    resumo = df.groupby("categoria")["valor"].sum().reset_index()
    resumo["percentual"] = resumo["valor"] / resumo["valor"].sum() * 100

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Detalhado", index=False)
        resumo.to_excel(writer, sheet_name="Resumo", index=False)

    # gráfico
    plt.figure(figsize=(6,6))
    resumo.set_index("categoria")["valor"].plot.pie(autopct="%1.1f%%", ylabel="")
    plt.title("Distribuição por Categoria")
    plt.savefig("grafico_categorias.png", dpi=200)
    plt.close()

    return output

