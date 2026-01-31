from pathlib import Path
import pandas as pd
import re
import zipfile

INPUT_ZIP = Path("data/final/consolidado_despesas.zip")
INPUT_CSV_NAME = "consolidado_despesas.csv"
OUTPUT_FILE = Path("data/processed/despesas_validadas.csv")


def is_valid_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r"\D", "", str(cnpj))

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calc_digit(cnpj, weights):
        s = sum(int(d) * w for d, w in zip(cnpj, weights))
        r = s % 11
        return "0" if r < 2 else str(11 - r)

    d1 = calc_digit(cnpj[:12], [5,4,3,2,9,8,7,6,5,4,3,2])
    d2 = calc_digit(cnpj[:13], [6,5,4,3,2,9,8,7,6,5,4,3,2])

    return cnpj[-2:] == d1 + d2


def main():
    with zipfile.ZipFile(INPUT_ZIP) as z:
        with z.open(INPUT_CSV_NAME) as f:
            df = pd.read_csv(f, encoding="utf-8-sig")

    df["CNPJ"] = df["CNPJ"].astype(str)
    df["RazaoSocial"] = df["RazaoSocial"].astype(str)

    df = df[df["RazaoSocial"].str.strip() != ""]
    df = df[df["ValorDespesas"] > 0]
    df = df[df["CNPJ"].apply(is_valid_cnpj)]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"✅ Dados validados: {len(df)} registros salvos em {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
