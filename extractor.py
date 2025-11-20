# extractor.py
import re
import pdfplumber
import pandas as pd

def normalizar_valor(v):
    v = v.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(v)
    except:
        return None


def parse_data_nubank(data_str):
    meses = {
        "JAN": "01", "FEV": "02", "MAR": "03", "ABR": "04",
        "MAI": "05", "JUN": "06", "JUL": "07", "AGO": "08",
        "SET": "09", "OUT": "10", "NOV": "11", "DEZ": "12"
    }
    dia, mes = data_str.split()
    ano = "2025"  # depois automação
    return f"{dia}/{meses[mes]}/{ano}"


def extrair_transacoes_pdf(caminho_pdf):

    # Formato Nubank (exemplo):
    # 12 JAN   PADARIA DO ZE         R$ 25,30
    padrao = re.compile(
        r"(\d{2}\s+[A-Z]{3})\s+(.+?)\s+R\$\s*([0-9\.,]+)"
    )

    resultados = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()

            if not texto:
                continue

            for linha in texto.split("\n"):
                m = padrao.search(linha)
                if m:
                    data, descricao, valor = m.groups()

                    resultados.append({
                        "data": parse_data_nubank(data),
                        "descricao": descricao.strip(),
                        "valor": normalizar_valor(valor)
                    })

    df = pd.DataFrame(resultados)

    # remove linhas sem valor
    if "valor" in df.columns:
        df = df[df["valor"].notna()]

    # normaliza espaços pra facilitar os filtros
    df["descricao"] = df["descricao"].str.replace(r"\s+", " ", regex=True).str.strip()

    # remove linhas que não são transações (ex: "a 09 NOV")
    df = df[~df["descricao"].str.match(r"^a \d{2} [A-Z]{3}$")]

    # DEBUG
    print("\n--- DEBUG ---")
    print(df.head())
    print(df.columns)
    print("------------\n")

    return df


