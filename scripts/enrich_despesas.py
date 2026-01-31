from pathlib import Path
import pandas as pd
import requests

DESPESAS_FILE = Path("data/processed/despesas_validadas.csv")
CADASTRO_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
CADASTRO_FILE = Path("data/raw/operadoras_ativas.csv")
OUTPUT_FILE = Path("data/processed/despesas_enriquecidas.csv")


def normalize_cnpj(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.replace(r"\D", "", regex=True)
        .str.zfill(14)
    )


def main():
    df = pd.read_csv(DESPESAS_FILE)
    df["CNPJ"] = normalize_cnpj(df["CNPJ"])

    CADASTRO_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not CADASTRO_FILE.exists():
        print("⬇️ Baixando cadastro de operadoras...")
        r = requests.get(CADASTRO_URL)
        r.raise_for_status()
        CADASTRO_FILE.write_bytes(r.content)

    cadastro = pd.read_csv(CADASTRO_FILE, sep=";", encoding="latin1")
    cadastro.columns = cadastro.columns.str.upper()
    cadastro["CNPJ"] = normalize_cnpj(cadastro["CNPJ"])
    cadastro = cadastro.drop_duplicates(subset=["CNPJ"])

    enriched = df.merge(
        cadastro[["CNPJ", "REGISTRO_OPERADORA", "MODALIDADE", "UF"]],
        on="CNPJ",
        how="left"
    )

    enriched.rename(columns={
        "REGISTRO_OPERADORA": "RegistroANS",
        "MODALIDADE": "Modalidade"
    }, inplace=True)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"✅ Dados enriquecidos salvos em {OUTPUT_FILE}")
    print(f"📊 Registros sem cadastro: {enriched['RegistroANS'].isna().sum()}")


if __name__ == "__main__":
    main()
