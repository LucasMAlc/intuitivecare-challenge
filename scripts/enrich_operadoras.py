from pathlib import Path
import pandas as pd

DESPESAS_FILE = Path("data/processed/despesas_normalizadas.csv")
OPERADORAS_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
OUTPUT_FILE = Path("data/processed/despesas_enriquecidas.csv")


def main():
    print("📥 Lendo despesas normalizadas...")
    despesas = pd.read_csv(DESPESAS_FILE, dtype=str)

    print("📥 Baixando cadastro de operadoras ativas...")
    operadoras = pd.read_csv(
        OPERADORAS_URL,
        sep=";",
        encoding="latin1",
        dtype=str
    )

    # Seleciona apenas o necessário
    operadoras = operadoras[[
        "REGISTRO_OPERADORA",
        "CNPJ",
        "Razao_Social"
    ]]

    # Padroniza chave
    despesas["reg_ans"] = despesas["reg_ans"].astype(str)
    operadoras["REGISTRO_OPERADORA"] = operadoras["REGISTRO_OPERADORA"].astype(str)

    print("🔗 Enriquecendo dados pelo REGISTRO ANS...")
    enriched = despesas.merge(
        operadoras,
        left_on="reg_ans",
        right_on="REGISTRO_OPERADORA",
        how="left"
    )

    enriched.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Arquivo enriquecido salvo em {OUTPUT_FILE}")
    print(f"📊 Registros sem match: {enriched['CNPJ'].isna().sum()}")


if __name__ == "__main__":
    main()
