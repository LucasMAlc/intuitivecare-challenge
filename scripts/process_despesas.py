import zipfile
from pathlib import Path
import pandas as pd
import re
import unicodedata

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "despesas_normalizadas.csv"


def read_csv_tolerant(file_obj) -> pd.DataFrame:
    for enc in ["utf-8-sig", "utf-8", "latin1"]:
        try:
            file_obj.seek(0)
            return pd.read_csv(file_obj, sep=";", encoding=enc)
        except UnicodeDecodeError:
            continue
    raise RuntimeError("Não foi possível decodificar o arquivo CSV/TXT.")


def read_from_zip(zip_path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if name.lower().endswith((".csv", ".txt", ".xlsx")):
                with z.open(name) as f:
                    if name.lower().endswith(".xlsx"):
                        return pd.read_excel(f)
                    else:
                        return read_csv_tolerant(f)

    raise RuntimeError(f"Nenhum arquivo de dados encontrado em {zip_path.name}")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w_]", "", regex=True)
    )
    return df


def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include="object").columns:
        df[col] = (
            df[col]
            .astype(str)
            .apply(lambda x: unicodedata.normalize("NFC", x))
        )
    return df


def filter_despesas(df: pd.DataFrame) -> pd.DataFrame:
    candidatos = [
        c for c in df.columns
        if any(k in c for k in ["descricao", "ds_", "dsconta"])
    ]

    if not candidatos:
        raise RuntimeError("Coluna de descrição textual não encontrada.")

    coluna_desc = candidatos[0]

    mask = df[coluna_desc].astype(str).str.contains(
        r"evento|sinistro",
        case=False,
        na=False
    )

    return df[mask]


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    registros = []

    for zip_path in RAW_DIR.rglob("*.zip"):
        print(f"📦 Processando {zip_path.name}")

        df = read_from_zip(zip_path)
        df = normalize_columns(df)
        df = normalize_text_columns(df)
        df = filter_despesas(df)

        match = re.search(r"([1-4]T(\d{4}))", zip_path.name)
        if match:
            df["trimestre"] = match.group(1)
            df["ano"] = match.group(2)

        registros.append(df)

    if not registros:
        raise RuntimeError("Nenhuma despesa com eventos/sinistros encontrada.")

    final_df = pd.concat(registros, ignore_index=True)
    final_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"✅ Despesas normalizadas salvas em {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
