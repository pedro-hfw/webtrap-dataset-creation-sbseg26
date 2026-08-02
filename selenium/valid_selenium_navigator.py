from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse, urlencode, urljoin
from urllib.robotparser import RobotFileParser
from pathlib import Path
import time, random, csv, argparse

# ------------------
# Adicionando Flags
# ------------------


parser = argparse.ArgumentParser(description = "Selenium Navegador")

parser.add_argument(
    "-r", "--repeats",
    type=int,
    default=10,
    help="Número de navegações por execução"
)

args = parser.parse_args()


# --------------------------
# Configurações do Selenium
# --------------------------

# Alterar para o site escolhido

SITE = "example"

INITIAL_URL  = f"https://www.{SITE}.com.br/"
DOMAIN       = f"{SITE}.com.br"

# Output do CSV de requisições
BASE_DIR     = Path(__file__).resolve().parent
ROOT_DIR     = BASE_DIR.parent
OUTPUT_CSV   = str(ROOT_DIR / "generated_requests" / "VALID_Selenium_GETS.csv")

# Alterar para seu diretório do Geckodriver
GECKODRIVER_DIR = "/usr/local/bin/geckodriver"

NAV_STEPS    = args.repeats       # passos de navegação aleatória
FORM_STEPS   = 10                 # quantos formulários submeter por página
USER_AGENT   = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) "
                "Gecko/20100101 Firefox/124.0")

# Extensões de recursos estáticos que não interessam ao dataset
STATIC_EXTENSIONS = (
    ".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".svg",
    ".woff", ".woff2", ".ttf", ".ico", ".webp", ".mp4", ".pdf",
    ".map", ".json",
)

# Caminhos que indicam backend/API (não representam navegação humana)
BLOCKED_PATHS = (
    "cart", "services", "refactoring", "api", "lista-de-desejos",
    "listas", "intake", "auth", "wishlist", "checkout", "login",
    "account", "oauth", "static", "cdn", "atendimento"
)

# Valores sintéticos realistas para preencher campos de formulário
SYNTHETIC_VALUES = {
    "search":   ["notebook", "tênis corrida", "camiseta", "mochila"],
    "q":        ["notebook gamer", "celular samsung", "fone bluetooth"],
    "query":    ["tênis masculino", "notebook i5", "bermuda"],
    "category": ["esportes", "moda", "tecnologia"],
    "page":     ["1", "2", "3"],
    "sort":     ["price_asc", "relevance", "newest"],
    "size":     ["P", "M", "G", "GG"],
    "color":    ["preto", "branco", "azul"],
    "brand":    ["Nike", "Adidas", "Puma"],
    "min_price":["50", "100", "200"],
    "max_price":["300", "500", "1000"],
    "gender":   ["masculino", "feminino", "unissex"],
    # campos desconhecidos
    "_default": ["test", "exemplo", "1"],
}


# Funções Auxiliares
def get_synthetic_value(field_name: str) -> str:
    key = field_name.lower()
    for k, values in SYNTHETIC_VALUES.items():
        if k in key:
            return random.choice(values)
    return random.choice(SYNTHETIC_VALUES["_default"])


def is_static_resource(url: str) -> bool:
    path = urlparse(url).path.lower()
    return path.endswith(STATIC_EXTENSIONS)


def is_valid_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url)
    # Apenas http/https
    if parsed.scheme not in ("http", "https"):
        return False
    # Deve pertencer ao site alvo
    if SITE not in parsed.netloc:
        return False
    # Sem caminhos de backend/API
    if any(b in parsed.path.lower() for b in BLOCKED_PATHS):
        return False
    # Sem recursos estáticos
    if is_static_resource(url):
        return False
    return True

# Verifica se URL tem parâmetros
def has_param(url: str) -> bool:
    return bool(urlparse(url).query)

# Extrai campos interessantes
def extract_for_ml(url: str, method: str = "GET") -> dict | None:
    parsed = urlparse(url)
    if not parsed.query:
        return None
    return {
        "class":  "Valid",
        "method": method.upper(),
        "path":   parsed.path,
        "params": parsed.query,
    }

# Verifica robots da URL
def check_robots(base_url: str, user_agent: str = "*") -> RobotFileParser:
    rp = RobotFileParser()
    robots_url = urljoin(base_url, "/robots.txt")
    rp.set_url(robots_url)
    try:
        rp.read()
        print(f"[robots.txt] carregado de {robots_url}")
    except Exception as e:
        print(f"[robots.txt] erro ao ler: {e}")
    return rp


# Fonte 1 e 3 - Formulários GET
def collect_from_forms(driver, wait, rp: RobotFileParser, max_forms: int = 10) -> list[dict]:
    results = []

    forms = driver.find_elements(By.TAG_NAME, "form")
    get_forms = [f for f in forms if f.get_attribute("method").lower() in ("get", "")]

    print(f"[forms] {len(get_forms)} formulários GET encontrados")

    # Procura formulários para preencher
    for i, form in enumerate(get_forms[:max_forms]):
        action  = form.get_attribute("action") or driver.current_url
        inputs  = form.find_elements(By.TAG_NAME, "input")
        selects = form.find_elements(By.TAG_NAME, "select")

        params = {}

        for inp in inputs:
            inp_type = (inp.get_attribute("type") or "text").lower()
            inp_name = inp.get_attribute("name")
            if not inp_name:
                continue
            if inp_type in ("hidden", "submit", "button", "image", "reset"):
                if inp_type == "hidden":
                    params[inp_name] = inp.get_attribute("value") or ""
                continue
            params[inp_name] = get_synthetic_value(inp_name)

        for sel in selects:
            sel_name = sel.get_attribute("name")
            if not sel_name:
                continue
            options = sel.find_elements(By.TAG_NAME, "option")
            non_empty = [o.get_attribute("value") for o in options if o.get_attribute("value")]
            params[sel_name] = non_empty[0] if non_empty else ""

        if not params:
            continue

        # Monta a URL que o formulário geraria
        query_string = urlencode({k: v for k, v in params.items() if v})
        if not query_string:
            continue

        # Normaliza a URL
        if not action.startswith("http"):
            action = urljoin(driver.current_url, action)

        full_url = f"{action}?{query_string}"

        if not is_valid_url(full_url):
            continue

        entry = extract_for_ml(full_url)
        if entry:
            results.append(entry)
            print(f"[forms] form {i+1}: {full_url[:80]}")

    print(f"[forms] {len(results)} entradas coletadas")
    return results

# Fonte 2 - Navegação aleatória
def random_navigation(driver, wait, rp: RobotFileParser, steps: int = 10) -> list[dict]:
    results = []
    restart = 0

    for step in range(steps):
        print(f"[nav] passo {step + 1}/{steps}")
        # Simula atraso humano
        time.sleep(random.uniform(2, 5))

        links = driver.find_elements(By.TAG_NAME, "a")

        valid_links = []

        # Verifica se há parâmetros em alguma URL coletada
        for link in links:
            href = link.get_attribute("href")
            if href and is_valid_url(href) and has_param(href):
                valid_links.append((link, href))

        if not valid_links:
            print("[nav] nenhum link válido com parâmetros na página atual")
            restart += 1
            if restart == 2:
                restart = 0
                print("[nav] voltando para URL inicial")

                try:
                    driver.get(INITIAL_URL)
                except Exception as e:
                    print(f"[nav] erro ao voltar para URL inicial")

            continue

        # Escolhe alguma URL com parâmetros para clicar
        element, href = random.choice(valid_links)
        print(f"[nav] clicando em: {href[:80]}")

        try:
            driver.get(href)

            # Simula atraso humano  
            time.sleep(random.uniform(2, 4))

            current_url = driver.current_url
            if is_valid_url(current_url) and has_param(current_url):
                entry = extract_for_ml(current_url)
                if entry:
                    results.append(entry)

        except Exception as e:
            print(f"[nav] erro ao navegar: {e}")
            continue

    print(f"[nav] {len(results)} requisições coletadas")
    return results


# Fonte 4 - requests interceptados pelo seleniumwire
def collect_from_wire(driver) -> list[dict]:
    results = []
    seen = set()

    for req in driver.requests:
        if req.method != "GET":
            continue
        if not req.response:
            continue
        url = req.url
        if not is_valid_url(url):
            continue
        if not has_param(url):
            continue
        # Deduplicação por path+params
        parsed = urlparse(url)
        key = f"{parsed.path}?{parsed.query}"
        if key in seen:
            continue
        seen.add(key)

        entry = extract_for_ml(url)
        if entry:
            results.append(entry)

    print(f"[wire] {len(results)} requisições capturadas pelo seleniumwire")
    return results


# Main

def main():

    print(f"\nIniciando navegação em {INITIAL_URL} com {NAV_STEPS} repetições.\n")

    # Robots.txt
    rp = check_robots(INITIAL_URL)

    # Driver
    service = Service(GECKODRIVER_DIR)
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.set_preference("general.useragent.override", USER_AGENT)

    driver = webdriver.Firefox(service=service, options=options)
    wait   = WebDriverWait(driver, 10)

    all_entries = []

    try:
        # Carrega a página inicial
        driver.get(INITIAL_URL)
        time.sleep(3)

        # Fonte 1: formulários GET na página inicial
        form_entries_home = collect_from_forms(driver, wait, rp, max_forms=FORM_STEPS)
        all_entries.extend(form_entries_home)

        # Fonte 2: navegação aleatória
        nav_entries = random_navigation(driver, wait, rp, steps=NAV_STEPS)
        all_entries.extend(nav_entries)

        # Fonte 3: formulários nas páginas visitadas
        form_entries_nav = collect_from_forms(driver, wait, rp, max_forms=FORM_STEPS)
        all_entries.extend(form_entries_nav)

        # Fonte 4: requisições capturadas pelo seleniumwire
        wire_entries = collect_from_wire(driver)
        all_entries.extend(wire_entries)

    finally:
        driver.quit()

    # Deduplicação global por path+params
    seen_keys = set()
    unique_entries = []
    for e in all_entries:
        key = f"{e['path']}?{e['params']}"
        if key not in seen_keys:
            seen_keys.add(key)
            unique_entries.append(e)

    print(f"\n[resultado] {len(unique_entries)} entradas únicas coletadas")

    # Salvamento CSV
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["class", "method", "path", "params"],
                                delimiter="«")
        if f.tell() == 0:
            writer.writeheader()
        writer.writerows(unique_entries)

    print(f"[csv] salvo em {OUTPUT_CSV}")

    # Preview
    print("\n── Amostra das primeiras 5 entradas ──")
    for e in unique_entries[:5]:
        print(f"  {e['class']:7} « {e['method']:4} « {e['params'][:50]}")


if __name__ == "__main__":
    main()
