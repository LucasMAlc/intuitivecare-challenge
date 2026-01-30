from pathlib import Path
import pandas as pd
import zipfile

# ⚠️ Arquivo correto: enriquecido
INPUT_FILE = Path("data/processed/despesas_enriquecidas.csv")
OUTPUT_DIR = Path("data/final")
OUTPUT_ZIP = OUTPUT_DIR / "consolidado_despesas.zip"
OUTPUT_CSV_NAME = "consolidado_despesas.csv"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("📥 Lendo despesas enriquecidas...")
    df = pd.read_csv(INPUT_FILE, dtype=str)

    # --- Conversão do valor monetário ---
    df["ValorDespesas"] = (
        df["vl_saldo_final"]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # --- DataFrame final conforme enunciado ---
    final_df = pd.DataFrame({
        "CNPJ": df["CNPJ"],
        "RazaoSocial": df["Razao_Social"],
        "Trimestre": df["trimestre"],
        "Ano": df["ano"],
        "ValorDespesas": df["ValorDespesas"]
    })

    # --- Consolidação (não descartar NaN) ---
    consolidado = (
        final_df
        .groupby(
            ["CNPJ", "RazaoSocial", "Trimestre", "Ano"],
            dropna=False,
            as_index=False
        )["ValorDespesas"]
        .sum()
    )

    # --- Escrita e compactação ---
    csv_content = consolidado.to_csv(index=False)

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(OUTPUT_CSV_NAME, csv_content)

    print(f"✅ Arquivo final gerado em {OUTPUT_ZIP}")
    print(f"📊 Linhas consolidadas: {len(consolidado)}")


if __name__ == "__main__":
    main()
