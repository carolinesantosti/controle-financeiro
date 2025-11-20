# main.py
from finance import registrar_transacao, calcular_saldo, gerar_relatorio
from extractor import extrair_transacoes_pdf
from categorizer import categorizar_descricao
from export import gerar_excel
import os

def importar_fatura_pdf():
    caminho = input("Caminho do PDF: ").strip()

    if not os.path.exists(caminho):
        print("Arquivo não encontrado.")
        return

    df = extrair_transacoes_pdf(caminho)

    if df.empty:
        print("Nenhuma transação encontrada no PDF.")
        return

    df["categoria"] = df["descricao"].apply(categorizar_descricao)

    for _, row in df.iterrows():
        tipo = "despesa" if row["valor"] < 0 else "receita"
        registrar_transacao(tipo, abs(row["valor"]), row["descricao"])

    gerar_excel(df)

    print("Fatura importada com sucesso!")
    print("Planilha gerada: dados_processados.xlsx")
    print("Gráfico gerado: grafico_categorias.png")

def menu():
    while True:
        print("\n======== CONTROLE FINANCEIRO ========")
        print("1 - Registrar despesa")
        print("2 - Registrar receita")
        print("3 - Ver saldo")
        print("4 - Gerar relatório")
        print("5 - Importar fatura PDF")
        print("6 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            valor = float(input("Valor: R$ "))
            desc = input("Descrição: ")
            registrar_transacao("despesa", valor, desc)
            print("Despesa registrada!")

        elif opcao == "2":
            valor = float(input("Valor: R$ "))
            desc = input("Descrição: ")
            registrar_transacao("receita", valor, desc)
            print("Receita registrada!")

        elif opcao == "3":
            saldo = calcular_saldo()
            print(f"Saldo atual: R$ {saldo:.2f}")

        elif opcao == "4":
            print(gerar_relatorio())

        elif opcao == "5":
            importar_fatura_pdf()

        elif opcao == "6":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
