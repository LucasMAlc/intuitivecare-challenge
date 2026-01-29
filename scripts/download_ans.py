import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
OUTPUT_DIR = Path("data/raw")


def get_soup(url: str) -> BeautifulSoup:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def list_years() -> list[str]:
    soup = get_soup(BASE_URL)
    years = []

    for a in soup.find_all("a", href=True):
        name = a["href"].strip("/")

        if re.fullmatch(r"\d{4}", name):
            years.append(name)

    return sorted(years, reverse=True)


def list_quarter_zips(year: str) -> list[str]:
    soup = get_soup(f"{BASE_URL}{year}/")
    zips = []

    for a in soup.find_all("a", href=True):
        name = a["href"]

        if re.fullmatch(r"[1-4]T\d{4}\.zip", name):
            zips.append(name)

    return sorted(zips, reverse=True)


def get_last_quarter_files(limit: int = 3) -> list[tuple[str, str]]:
    files = []

    for year in list_years():
        for zip_name in list_quarter_zips(year):
            files.append((year, zip_name))
            if len(files) == limit:
                return files

    return files


def download_file(year: str, filename: str):
    url = f"{BASE_URL}{year}/{filename}"
    target_dir = OUTPUT_DIR / year
    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / filename

    if file_path.exists():
        return

    print(f"⬇️ Baixando {year}/{filename}")
    r = requests.get(url, stream=True)
    r.raise_for_status()

    with open(file_path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("🔎 Identificando últimos 3 trimestres disponíveis...")
    files = get_last_quarter_files()

    for year, filename in files:
        download_file(year, filename)

    print("✅ Download finalizado com sucesso.")


if __name__ == "__main__":
    main()
