import random, csv, urllib.parse, argparse
from pathlib import Path
from payloads import *

# ------------------
# Adicionando Flags
# ------------------

parser = argparse.ArgumentParser(description = "Gerador de Tráfego de Fórum [MALICIOSO]")

parser.add_argument(
    "-r", "--requests",
    type=int,
    default=3000,
    help="Número de requisições para gerar"
)

parser.add_argument(
    "-s", "--simple",
    action="store_true",
    help="Codifica requisição uma vez"
)

parser.add_argument(
    "-d", "--double",
    action="store_true",
    help="Codifica requisição duas vezes"
)

args = parser.parse_args()

# -----------------------
# Configuração
# -----------------------

if (args.simple and args.double):
    print("ALERTA: Escolha apenas uma forma de codificação.")
    exit(1)

BASE_DIR     = Path(__file__).resolve().parent
OUTPUT_CSV   = str(BASE_DIR / "generated_requests" / "ANOMALOUS_Forum_GETS.csv")

# Quantidade de requisições para gerar
TO_GENERATE = args.requests

# Alterar para o ataque desejado
PAYLOAD = SQLI_TERMS

typeof = ["comments", "users", "posts", "media"]

def generate_query():
    base = []

    malicious_payload = (random.choice(PAYLOAD).replace(' ', '+').replace('\n', '%0A')
                   .replace('\r', '%0D').replace('\033', '%1B'))

    # ENCODING
    if(args.simple):
        malicious_payload = (urllib.parse.quote(malicious_payload))

    # DOUBLE ENCODING
    if(args.double):
        malicious_payload = urllib.parse.quote(urllib.parse.quote(malicious_payload)) 

    base.append(f"q={malicious_payload}{random.choice(SEARCH_TERMS).replace(' ', '+')}")
    
    base.append(f"type={random.choice(typeof)}")
    
    if random.random() < 0.7:
        base.append(random.choice([
            "sort=top",
            "sort=bottom",
            "sort=recent"
    ]))

    if random.random() < 0.3:
        base.append(random.choice([
            "t=hour",
            "t=day",
            "t=month",
            "t=year"
    ]))
    
    return "&".join(base)

entries = []

for i in range(TO_GENERATE):
    params = generate_query()
    if not params == "":
        entries.append({"class": "Anomalous", "method": "GET", "params": params})


with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["class", "method", "params"],
                            delimiter="«", quoting=csv.QUOTE_NONE,
                            escapechar="\\")
    if f.tell() == 0:
        writer.writeheader()
    
    for e in entries:
        writer.writerow(e)

print(f"[csv] salvo em {OUTPUT_CSV}")