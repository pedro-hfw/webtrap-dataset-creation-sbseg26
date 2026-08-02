import random, csv, argparse
from pathlib import Path
from payloads import *

# ------------------
# Adicionando Flags
# ------------------

parser = argparse.ArgumentParser(description = "Gerador de Tráfego de Login")

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
OUTPUT_CSV   = str(BASE_DIR / "generated_requests" / "VALID_Login_POSTS.csv")

# Baixados separadamente
WORDLIST_PATH = str(BASE_DIR / "rockyou.txt")
USERNAME_PATH = str(BASE_DIR / "top-usernames-shortlist.txt")

TO_GENERATE = args.requests

def load_wordlist(filepath, max_words=10000):

    with open(filepath, "r", encoding="latin-1") as f:
        words = [line.strip() for line in f]
        
    return words[:max_words]

def generate_username():

    prefixes = ["user", "admin", "client", "test", "guest", "root", "usuario", "administrador", 
                "ubuntu", "teste", "r00t", "mysql", ""]
    
    suffix = random.randint(1, 9999)

    return random.choice(prefixes) + str(suffix)

def generate_email(username):

    domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "ymail.com"]

    return f"{username}@{random.choice(domains)}"

def generate_post_data(password_list, username_list):

    username = random.choice(username_list) + str(random.randint(1, 999))
    password = random.choice(password_list)

    # Ajustar para gerar variedade
    formats = [
        f"username={username}&password={password}",
        f"user={username}&pass={password}",
        f"email={generate_email(username)}&password={password}",
        f"login={username}&pwd={password}&remember=true",
        f"username={username}&password={password}&csrf_token={random.randint(100000,999999)}"
    ]
    
    return random.choice(formats)

def generate_dataset(wordlist_path, username_path, n_samples=2000):

    usernames = load_wordlist(username_path)
    passwords = load_wordlist(wordlist_path)
    entries = []

    for _ in range(n_samples):
        post_data = generate_post_data(passwords, usernames)
        entries.append({"class": "Valid", "method": "POST", "params": post_data})

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