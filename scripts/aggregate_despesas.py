from pathlib import Path
import pandas as pd
import zipfile

INPUT_FILE = Path("data/processed/despesas_enriquecidas.csv")
OUTPUT_DIR = Path("data/final")
OUTPUT_CSV = OUTPUT_DIR / "despesas_agregadas.csv"
OUTPUT_ZIP = OUTPUT_DIR / "Teste_Lucas.zip"


def main():
    df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")

    agg = (
        df.groupby(["RazaoSocial", "UF"], as_index=False)
        .agg(
            TotalDespesas=("ValorDespesas", "sum"),
            MediaTrimestral=("ValorDespesas", "mean"),
            DesvioPadrao=("ValorDespesas", "std")
        )
        .sort_values("TotalDespesas", ascending=False)
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    agg.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(OUTPUT_CSV, arcname="despesas_agregadas.csv")

    print(f"✅ Agregação concluída e compactada em {OUTPUT_ZIP}")


if __name__ == "__main__":
    main()
