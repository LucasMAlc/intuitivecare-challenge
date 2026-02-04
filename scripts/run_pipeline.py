import subprocess
import sys

steps = [
    # --- TESTE 1 ---
    "scripts/download_ans.py",
    "scripts/process_despesas.py",
    "scripts/enrich_operadoras.py",
    "scripts/consolidate_despesas.py",

    # --- TESTE 2 ---
    "scripts/validate_despesas.py",
    "scripts/enrich_despesas.py",
    "scripts/aggregate_despesas.py",
]

for step in steps:
    print(f"\n Executando {step}")
    result = subprocess.run([sys.executable, step])

    if result.returncode != 0:
        print(f"Erro em {step}. Pipeline interrompido.")
        break
else:
    print("\n✅ Pipeline executado com sucesso!")
