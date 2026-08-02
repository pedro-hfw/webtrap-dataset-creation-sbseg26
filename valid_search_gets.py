import random, csv, argparse
from pathlib import Path
from payloads import *

# ------------------
# Adicionando Flags
# ------------------

parser = argparse.ArgumentParser(description = "Gerador de Tráfego de Busca")

parser.add_argument(
    "-r", "--requests",
    type=int,
    default=3000,
    help="Número de requisições para gerar"
)

args = parser.parse_args()

# -----------------------
# Configuração
# -----------------------

BASE_DIR     = Path(__file__).resolve().parent
OUTPUT_CSV   = str(BASE_DIR / "generated_requests" / "VALID_Search_GETS.csv")

# Quantidade de requisições para gerar
TO_GENERATE = args.requests

# Modificar o código como quiser para gerar variedades de requisições
def generate_valid_query():
    base = []

    if random.random():
        base.append(f"search={random.choice(SEARCH_TERMS).replace(' ', '+')}")
    
    if random.random() < 0.6:
        base.append(f"id={random.randint(1, 500)}")

    if random.random() < 0.5:
        base.append(f"page={random.randint(1, 100)}")
    
    if random.random() < 0.4:
        base.append(f"action=view")
    
    if random.random() < 0.3:
        base.append(random.choice([
            "client=firefox-b-lm",
            "client=chrome",
            "client=brave",
            "client=opera",
            "client=duckduckgo"
    ]))

    if random.random() < 0.2:
        base.append(random.choice([
            "sort=price_asc",
            "sort=price_desc",
            "sort=rating"
        ]))

    return "&".join(base)

entries = []

for i in range(TO_GENERATE):
    params = generate_valid_query()
    if not params == "":
        entries.append({"class": "Valid", "method": "GET", "params": params})

with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["class", "method", "params"],
                            delimiter="«", quoting=csv.QUOTE_NONE,
                            escapechar="\\")
    if f.tell() == 0:
        writer.writeheader()
    
    for e in entries:
        writer.writerow(e)

print(f"[csv] salvo em {OUTPUT_CSV}")