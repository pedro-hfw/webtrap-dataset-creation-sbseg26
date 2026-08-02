import random, csv, argparse
from pathlib import Path
from payloads import *

# ------------------
# Adicionando Flags
# ------------------

parser = argparse.ArgumentParser(description = "Gerador de Tráfego de Fórum")

parser.add_argument(
    "-r", "--requests",
    type=int,
    default=3000,
    help="Número de requisições para gerar"
)

# -----------------------
# Configuração
# -----------------------

args = parser.parse_args()

BASE_DIR     = Path(__file__).resolve().parent
OUTPUT_CSV   = str(BASE_DIR / "generated_requests" / "VALID_Forum_GETS.csv")

# Quantidade de requisições para gerar
TO_GENERATE = args.requests

typeof = ["comments", "users", "posts", "media"]

def generate_realistic_query():
    base = []
    
    base.append(f"q={random.choice(SEARCH_TERMS).replace(' ', '+')}")
    
    base.append(f"type={random.choice(typeof)}")
    
    if random.random() < 0.7:
        base.append(random.choice([
            "sort=top",
            "sort=bottom",
            "sort=recent",
            "sort=controversial"
    ]))

    if random.random() < 0.3:
        base.append(random.choice([
            "t=hour",
            "t=day",
            "t=month",
            "t=year",
            "t=all"
    ]))
    
    return "&".join(base)

entries = []

for i in range(TO_GENERATE):
    params = generate_realistic_query()
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