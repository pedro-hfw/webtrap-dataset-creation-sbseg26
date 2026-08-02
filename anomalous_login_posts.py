import random, csv, urllib.parse, argparse
from pathlib import Path
from payloads import *

# ------------------
# Adicionando Flags
# ------------------

parser = argparse.ArgumentParser(description = "Gerador de Tráfego de Login [MALICIOSO]")

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
OUTPUT_CSV   = str(BASE_DIR / "generated_requests" / "ANOMALOUS_Login_POSTS.csv")

WORDLIST_PATH = str(BASE_DIR / "rockyou.txt")
USERNAME_PATH = str(BASE_DIR / "top-usernames-shortlist.txt")

TO_GENERATE = args.requests

PAYLOAD = SQLI_TERMS

# Auxiliares

def load_wordlist(filepath, max_words=10000):

    with open(filepath, "r", encoding="latin-1") as f:
        words = [line.strip() for line in f]

    return words[:max_words]

def generate_username():

    prefixes = ["user", "admin", "client", "test", "guest"]
    suffix = random.randint(1, 9999)

    return random.choice(prefixes) + str(suffix)

def generate_email(username):

    domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]

    return f"{username}@{random.choice(domains)}"



def generate_post_data(password_list, username_list):

    username = random.choice(username_list) + str(random.randint(1, 999))
    password = random.choice(password_list)

    malicious_payload = (random.choice(PAYLOAD).replace(' ', '+').replace('\n', '%0A')
                   .replace('\r', '%0D').replace('\033', '%1B'))

    # ENCODING
    if(args.simple):
        malicious_payload = (urllib.parse.quote(malicious_payload))

    # DOUBLE ENCODING
    if(args.double):
        malicious_payload = urllib.parse.quote(urllib.parse.quote(malicious_payload)) 

    # Ajustar para gerar variedade
    formats = [
        f"username={username}&password={malicious_payload}",
        f"user={username}&pass={malicious_payload}",
        f"email={generate_email(username)}&password={malicious_payload}",
        f"login={username}&pwd={malicious_payload}&remember=true",
        f"username={username}&password={malicious_payload}&csrf_token={random.randint(100000,999999)}"
    ]
    
    return random.choice(formats)



def generate_dataset(wordlist_path, username_path, n_samples=2000):
    usernames = load_wordlist(username_path)
    passwords = load_wordlist(wordlist_path)
    entries = []

    for _ in range(n_samples):
        post_data = generate_post_data(passwords, usernames)
        entries.append({"class": "Anomalous", "method": "POST", "params": post_data})

    return entries





if __name__ == "__main__":

    samples = generate_dataset(WORDLIST_PATH, USERNAME_PATH, TO_GENERATE)

with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["class", "method", "params"],
                            delimiter="«", quoting=csv.QUOTE_NONE,
                            escapechar="\\")
    if f.tell() == 0:
        writer.writeheader()
    
    for e in samples:
        writer.writerow(e)

print(f"[csv] salvo em {OUTPUT_CSV}")