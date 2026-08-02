from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import time, random, csv, argparse
from payloads import *

# ------------------
# Adicionando Flags
# ------------------


parser = argparse.ArgumentParser(description = "Selenium Navegador com Flask [MALICIOSO]")

parser.add_argument(
    "-r", "--repeats",
    type=int,
    default=5,
    help="Número de formulários preenchidos"
)

args = parser.parse_args()


# --------------
# Configurações
# --------------

# URL do Flask
BASE_URL     = "http://127.0.0.1:5000"

# Alterar para diretório do Geckodriver
SERVICE_PATH = "/usr/local/bin/geckodriver"

# Output do CSV de requisições
BASE_DIR     = Path(__file__).resolve().parent
ROOT_DIR     = BASE_DIR.parent
OUTPUT_CSV   = str(ROOT_DIR / "generated_requests" / "ANOMALOUS_Selenium_POSTS.csv")

REPEATS      = args.repeats   # quantas vezes preencher cada formulário com valores diferentes

# Alterar para o ataque desejado
PAYLOAD = SQLI_TERMS

# Dados Sintéticos
NAMES = [
    "João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa",
    "Lucas Ferreira", "Juliana Lima", "Rafael Souza", "Camila Rocha",
    "Bruno Carvalho", "Fernanda Alves", "Gustavo Mendes", "Letícia Pereira",
    "Rodrigo Martins", "Beatriz Gomes", "Felipe Barbosa", "Amanda Ribeiro",
    "Thiago Nascimento", "Carolina Araújo", "Eduardo Cardoso", "Isabela Moreira",
    "Marcelo Cunha", "Priscila Dias", "Vinicius Teixeira", "Larissa Nunes",
    "Renato Monteiro", "Vanessa Freitas", "Diego Correia", "Natalia Andrade",
    "Fabio Cavalcanti", "Gabriela Pinto",
]
EMAILS = [
    "joao@gmail.com", "maria@outlook.com", "pedro@yahoo.com",
    "ana@empresa.com.br", "lucas@hotmail.com", "juliana@uol.com.br",
    "rafael.souza@gmail.com", "camila.rocha@hotmail.com",
    "bruno.carvalho@yahoo.com.br", "fernanda_alves@outlook.com",
    "gustavo.mendes@empresa.com.br", "leticia.pereira@gmail.com",
    "rodrigo.martins99@gmail.com", "beatriz.gomes@uol.com.br",
    "felipe_barbosa@hotmail.com", "amanda.ribeiro@terra.com.br",
    "thiago.nascimento@ig.com.br", "carolina.araujo@gmail.com",
    "eduardo.cardoso@outlook.com", "isabela.moreira@yahoo.com",
]
PASSWORDS = [
    "Senha@2024!", "MinhaS3nha#", "Acesso123$", "P@ssw0rd2024",
    "Segura@321", "Forte#2025!", "MinhaConta99@", "Privado@456",
    "Secure!2024", "Login@Brasil1",
]
CEPS = [
    "01310-100", "20040-020", "30130-110", "90010-272", "41810-001",
    "80010-010", "69010-040", "74810-100", "50010-020", "60130-240",
    "13010-040", "40010-000", "88010-400", "57020-090", "49010-230",
]
STREET = [
    "Av. Paulista", "Rua das Flores", "Alameda Santos", "Rua XV de Novembro",
    "Av. Brasil", "Rua Sete de Setembro", "Rua da Consolação", "Av. Ipiranga",
    "Rua Augusta", "Av. Rebouças", "Rua Oscar Freire", "Rua Haddock Lobo",
    "Av. Brigadeiro Faria Lima", "Rua Vergueiro", "Av. Santo Amaro",
    "Rua Funchal", "Av. Berrini", "Rua João Dias", "Av. das Nações Unidas",
    "Rua da Paz",
]
COMPLEMENTOS = [
    "Apto 12", "Apto 304", "Casa 2", "Bloco B apto 5", "Cobertura",
    "Sala 202", "Fundos", "Casa", "Apto 801", "Bloco A apto 11",
]
CITY = [
    "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Porto Alegre",
    "Salvador", "Fortaleza", "Curitiba", "Manaus", "Recife", "Goiânia",
    "Belém", "Florianópolis", "São Luís", "Maceió", "Natal",
    "Teresina", "Campo Grande", "João Pessoa", "Aracaju", "Macapá",
]
STATE = [
    "SP", "RJ", "MG", "RS", "PR",
    "SC", "BA", "GO", "DF", "PE",
    "CE", "PA", "MA", "AL", "RN",
    "PB", "PI", "MS", "SE", "AP",
]
TERMS = [
    # eletrônicos
    "select notebook gamer", "notebook dell", "notebook samsung", "notebook and lenovo",
    "smartphone 5G", "not smartphone samsung", "iphone select 14", "iphone usado not",
    "fone bluetooth", "headphone and sem fio", "headset gamer",
    "monitor and 4K", "select monitor 27 polegadas", "teclado mecânico", "teclado sem fio",
    "mouse not gamer", "script mouse sem fio", "webcam full hd", "ssd externo",
    "pen drive and 64gb", "select carregador portatil", "cabo usb tipo c",
    "smartwatch", "not tablet samsung",
    # moda
    "tênis corrida", "tênis not nike", "tênis adidas", "tênis puma",
    "camiseta preta", "calça and jeans", "vestido floral", "jaqueta de couro",
    "moletom oversized", "legging select feminina", "sandalia and feminina",
    "bota coturno", "sapato social and masculino",
    # casa
    "panela not antiaderente", "jogo and de not cama", "edredom casal",
    "luminaria led", "tapete sala and", "garrafa select termica",
    # esporte
    "mochila escolar and", "câmera mirrorless", "kit alerta academia",
    "bola futebol", "raquete select beach not tennis", "bike script ergometrica",
    "suplemento whey protein", "colchonete yoga",
]
CATEGORY  = ["eletronicos", "esportes", "moda", "casa", "livros", "beleza", "games", "brinquedos"]
BRAND = [
    "Samsung", "Apple", "Nike", "Adidas", "Sony", "Dell", "LG",
    "Motorola", "Puma", "New Balance", "Lenovo", "Acer", "Asus",
    "Xiaomi", "JBL", "Philips", "Multilaser", "Positivo", "Havaianas",
]
MESSAGES = [
    "Gostaria de saber mais informações sobre meu pedido.",
    "Preciso de ajuda com a devolução do produto.",
    "O produto chegou com defeito, como proceder?",
    "Quando meu pedido será entregue?",
    "Adorei o produto, chegou antes do prazo!",
    "Não recebi o código de rastreamento do meu pedido.",
    "O produto recebido é diferente do anunciado.",
    "Quero cancelar meu pedido, ainda é possível?",
    "Fui cobrado duas vezes, como solicitar estorno?",
    "Preciso alterar o endereço de entrega do meu pedido.",
    "O boleto venceu, como gerar um novo?",
    "Meu cupom de desconto não foi aplicado.",
    "Como faço para trocar o tamanho do produto?",
    "O produto está disponível em outras cores?",
    "Gostaria de saber o prazo de garantia deste produto.",
]
COMMENTS = [
    "Produto excelente, superou minhas expectativas.",
    "Boa qualidade pelo preço, recomendo.",
    "Entrega rápida e produto bem embalado.",
    "Atendeu perfeitamente ao que eu precisava.",
    "Produto bom mas poderia ter melhor acabamento.",
    "Comprei para presente e a pessoa adorou.",
    "Material resistente, valeu a pena o investimento.",
    "Chegou em perfeitas condições, sem nenhum dano.",
    "Descrição condiz com o produto real, sem surpresas.",
    "Preço justo e ótimo custo-benefício.",
    "Poderia ter chegado melhor embalado.",
    "Qualidade acima do esperado para o valor pago.",
    "Produto original, sem indícios de falsificação.",
    "Funcionou perfeitamente desde o primeiro uso.",
    "Recomendo a todos que procuram qualidade e preço.",
]
CREDIT_CARD = [
    "4111 1111 1111 1111",  
    "5500 0000 0000 0004",  
    "3714 496353 98431",    
    "6011 1111 1111 1117",  
    "4012 8888 8888 1881",  
    "5105 1051 0510 5100",  
    "3782 822463 10005",    
]
USERNAMES = [
    "joao_silva42", "maria_s", "pedro.dev", "ana_costa99", "lucas_games",
    "camila_rocha", "rafael.souza", "brunoc_oficial", "fer_alves",
    "gustavo_m", "leti_pereira", "rod_martins", "bea_gomes",
    "felipeb_", "amanda.r99", "thiago_nsc", "carol_araujo",
    "edu.cardoso", "isa_moreira", "marceloc_",
]
BIOS = [
    "Apaixonado por tecnologia.",
    "Amante de esportes e natureza.",
    "Desenvolvedora e criadora de conteúdo.",
    "Curioso por natureza, geek por escolha.",
    "Fotógrafa amadora e viajante nas horas vagas.",
    "Estudante de engenharia e apaixonado por games.",
    "Mãe, empreendedora e entusiasta de bem-estar.",
    "Designer gráfico e colecionador de quadrinhos.",
    "Professor universitário e pesquisador de IA.",
    "Chef amador e amante de vinhos.",
    "Atleta de fim de semana e fã de séries.",
    "Advogada, leitora voraz e pet lover.",
]
COMMENT_TITLE = [
    "Ótima compra!", "Valeu cada centavo.", "Recomendo sem hesitar.",
    "Produto como descrito.", "Poderia ser melhor.",
    "Superou minhas expectativas!", "Muito satisfeito com a compra.",
    "Entrega rápida e produto perfeito.", "Bom custo-benefício.",
    "Comprarei novamente.", "Produto de qualidade.", "Decepcionante.",
    "Exatamente o que eu precisava.", "Atendimento excelente.",
    "Chegou antes do prazo!", "Produto original e bem embalado.",
]

# Escolhe um item aleatório de uma lista.
def rand(lst):
    return random.choice(lst)


def rand_number(min_val, max_val):
    return str(random.randint(min_val, max_val))


# Definição dos Formulários
def fill_login(driver, wait):
    ATTACK = rand(PAYLOAD)
    wait.until(EC.presence_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(ATTACK)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(rand(PASSWORDS))
    remember = random.choice(["yes", "no"])
    driver.find_element(By.CSS_SELECTOR, f"input[name='remember'][value='{remember}']").click()


def fill_register(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "first_name")))
    ATTACK = rand(PAYLOAD)
    nome = rand(NAMES).split()
    driver.find_element(By.ID, "first_name").clear()
    driver.find_element(By.ID, "first_name").send_keys(nome[0])
    driver.find_element(By.ID, "last_name").clear()
    driver.find_element(By.ID, "last_name").send_keys(nome[-1])
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(rand(EMAILS))
    driver.find_element(By.ID, "cpf").clear()
    driver.find_element(By.ID, "cpf").send_keys(f"{rand_number(100,999)}.{rand_number(100,999)}.{rand_number(100,999)}-{rand_number(10,99)}")
    driver.find_element(By.ID, "birthdate").send_keys(f"{rand_number(1970,2000)}-{rand_number(1,12):02}-{rand_number(1,28):02}")
    driver.find_element(By.ID, "phone").clear()
    driver.find_element(By.ID, "phone").send_keys(f"(21) 9{rand_number(7000,9999)}-{rand_number(1000,9999)}")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(ATTACK)
    driver.find_element(By.ID, "password_confirm").clear()
    driver.find_element(By.ID, "password_confirm").send_keys(ATTACK)
    gender = random.choice(["M", "F", "O"])
    driver.find_element(By.CSS_SELECTOR, f"input[name='gender'][value='{gender}']").click()
    # Marca alguns interesses aleatoriamente
    for val in ["tech", "sports", "fashion", "games"]:
        if random.random() > 0.5:
            cb = driver.find_element(By.CSS_SELECTOR, f"input[name='interests'][value='{val}']")
            if not cb.is_selected():
                cb.click()


def fill_search(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "q")))
    ATTACK = rand(PAYLOAD)
    driver.find_element(By.ID, "q").clear()
    driver.find_element(By.ID, "q").send_keys(rand(TERMS))
    Select(driver.find_element(By.ID, "category")).select_by_value(rand(CATEGORY))
    Select(driver.find_element(By.ID, "sort")).select_by_value(
        rand(["relevance", "price_asc", "price_desc", "newest", "rating"]))
    driver.find_element(By.ID, "min_price").clear()
    driver.find_element(By.ID, "min_price").send_keys(rand_number(0, 500))
    driver.find_element(By.ID, "max_price").clear()
    driver.find_element(By.ID, "max_price").send_keys(rand_number(500, 5000))
    condition = random.choice(["all", "new", "used", "refurbished"])
    driver.find_element(By.CSS_SELECTOR, f"input[name='condition'][value='{condition}']").click()
    driver.find_element(By.ID, "brand").clear()
    driver.find_element(By.ID, "brand").send_keys(ATTACK)
    driver.find_element(By.ID, "page").clear()
    driver.find_element(By.ID, "page").send_keys(rand_number(1, 10))


def fill_contact(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "name")))
    ATTACK = rand(PAYLOAD)
    driver.find_element(By.ID, "name").clear()
    driver.find_element(By.ID, "name").send_keys(rand(NAMES))
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(rand(EMAILS))
    Select(driver.find_element(By.ID, "subject")).select_by_value(
        rand(["support", "billing", "shipping", "return", "complaint", "suggestion", "other"]))
    driver.find_element(By.ID, "order_id").clear()
    driver.find_element(By.ID, "order_id").send_keys(f"PED-2024-{rand_number(10000,99999)}")
    priority = random.choice(["low", "normal", "high"])
    driver.find_element(By.CSS_SELECTOR, f"input[name='priority'][value='{priority}']").click()
    driver.find_element(By.ID, "message").clear()
    driver.find_element(By.ID, "message").send_keys(ATTACK)
    for val in ["email", "phone", "whatsapp"]:
        cb = driver.find_element(By.CSS_SELECTOR, f"input[name='contact_via'][value='{val}']")
        desired = random.random() > 0.4
        if cb.is_selected() != desired:
            cb.click()


def fill_profile(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "first_name")))
    ATTACK = rand(PAYLOAD)
    nome = rand(NAMES).split()
    driver.find_element(By.ID, "first_name").clear()
    driver.find_element(By.ID, "first_name").send_keys(nome[0])
    driver.find_element(By.ID, "last_name").clear()
    driver.find_element(By.ID, "last_name").send_keys(nome[-1])
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(rand(USERNAMES))
    driver.find_element(By.ID, "bio").clear()
    driver.find_element(By.ID, "bio").send_keys(ATTACK)
    driver.find_element(By.ID, "website").clear()
    driver.find_element(By.ID, "website").send_keys(f"https://meusite{rand_number(1,99)}.com.br")
    driver.find_element(By.ID, "cep").clear()
    driver.find_element(By.ID, "cep").send_keys(rand(CEPS))
    driver.find_element(By.ID, "street").clear()
    driver.find_element(By.ID, "street").send_keys(rand(STREET))
    driver.find_element(By.ID, "number").clear()
    driver.find_element(By.ID, "number").send_keys(rand_number(1, 9999))
    driver.find_element(By.ID, "city").clear()
    driver.find_element(By.ID, "city").send_keys(rand(CITY))
    Select(driver.find_element(By.ID, "state")).select_by_value(rand(STATE))
    Select(driver.find_element(By.ID, "language")).select_by_value(
        rand(["pt-BR", "en-US", "es"]))
    for val in ["email", "push", "sms"]:
        cb = driver.find_element(By.CSS_SELECTOR, f"input[name='notif'][value='{val}']")
        desired = random.random() > 0.4
        if cb.is_selected() != desired:
            cb.click()


def fill_checkout(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "recipient_name")))
    ATTACK = rand(PAYLOAD)
    driver.find_element(By.ID, "recipient_name").clear()
    driver.find_element(By.ID, "recipient_name").send_keys(ATTACK)
    driver.find_element(By.ID, "cep").clear()
    driver.find_element(By.ID, "cep").send_keys(rand(CEPS))
    driver.find_element(By.ID, "street").clear()
    driver.find_element(By.ID, "street").send_keys(rand(STREET))
    driver.find_element(By.ID, "number").clear()
    driver.find_element(By.ID, "number").send_keys(rand_number(1, 9999))
    driver.find_element(By.ID, "complement").clear()
    driver.find_element(By.ID, "complement").send_keys(f"Apto {rand_number(1,200)}")
    driver.find_element(By.ID, "city").clear()
    driver.find_element(By.ID, "city").send_keys(rand(CITY))
    Select(driver.find_element(By.ID, "state")).select_by_value(rand(STATE))
    Select(driver.find_element(By.ID, "shipping_method")).select_by_value(
        rand(["standard", "express", "same_day", "pickup"]))
    payment = random.choice(["credit", "debit", "pix", "boleto"])
    driver.find_element(By.CSS_SELECTOR, f"input[name='payment_method'][value='{payment}']").click()
    driver.find_element(By.ID, "card_number").clear()
    driver.find_element(By.ID, "card_number").send_keys(rand(CREDIT_CARD))
    driver.find_element(By.ID, "card_expiry").clear()
    driver.find_element(By.ID, "card_expiry").send_keys(f"{rand_number(1,12):02}/{rand_number(25,30)}")
    driver.find_element(By.ID, "card_cvv").clear()
    driver.find_element(By.ID, "card_cvv").send_keys(rand_number(100, 999))
    Select(driver.find_element(By.ID, "installments")).select_by_value(
        rand(["1", "2", "3", "6", "12"]))
    if random.random() > 0.7:
        driver.find_element(By.ID, "coupon").send_keys(f"PROMO{rand_number(5,30)}")


def fill_comment(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "author_name")))
    ATTACK = rand(PAYLOAD)
    driver.find_element(By.ID, "author_name").clear()
    driver.find_element(By.ID, "author_name").send_keys(rand(NAMES))
    driver.find_element(By.ID, "author_email").clear()
    driver.find_element(By.ID, "author_email").send_keys(rand(EMAILS))
    rating = rand(["1", "2", "3", "4", "5"])
    driver.find_element(By.CSS_SELECTOR, f"input[name='rating'][value='{rating}']").click()
    driver.find_element(By.ID, "title").clear()
    driver.find_element(By.ID, "title").send_keys(rand(COMMENT_TITLE))
    driver.find_element(By.ID, "body").clear()
    driver.find_element(By.ID, "body").send_keys(ATTACK)
    rec = random.choice(["yes", "no"])
    driver.find_element(By.CSS_SELECTOR, f"input[name='recommend'][value='{rec}']").click()
    for val in ["quality", "price", "delivery", "packaging"]:
        cb = driver.find_element(By.CSS_SELECTOR, f"input[name='aspects'][value='{val}']")
        desired = random.random() > 0.4
        if cb.is_selected() != desired:
            cb.click()


def fill_products(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "category")))
    ATTACK = rand(PAYLOAD)
    Select(driver.find_element(By.ID, "category")).select_by_value(
        rand(["all", "notebooks", "smartphones", "tablets", "tvs", "cameras", "headphones"]))
    Select(driver.find_element(By.ID, "brand")).select_by_value(
        rand(["", "samsung", "apple", "lg", "sony", "motorola", "dell"]))
    driver.find_element(By.ID, "min_price").clear()
    driver.find_element(By.ID, "min_price").send_keys(rand_number(0, 500))
    driver.find_element(By.ID, "max_price").clear()
    driver.find_element(By.ID, "max_price").send_keys(rand_number(500, 10000))
    avail = random.choice(["all", "in_stock", "pre_order"])
    driver.find_element(By.CSS_SELECTOR, f"input[name='availability'][value='{avail}']").click()
    for val in ["free_shipping", "discount", "new", "best_seller"]:
        cb = driver.find_element(By.CSS_SELECTOR, f"input[name='features'][value='{val}']")
        desired = random.random() > 0.5
        if cb.is_selected() != desired:
            cb.click()
    Select(driver.find_element(By.ID, "sort")).select_by_value(
        rand(["relevance", "price_asc", "price_desc", "newest", "best_seller"]))
    Select(driver.find_element(By.ID, "per_page")).select_by_value(rand(["12", "24", "48"]))


# Mapa: url -> função de preenchimento

FORMS = [
    ("/login",    "form-login",    fill_login),
    ("/register", "form-register", fill_register),
    ("/search",   "form-search",   fill_search),
    ("/contact",  "form-contact",  fill_contact),
    ("/profile",  "form-profile",  fill_profile),
    ("/checkout", "form-checkout", fill_checkout),
    ("/comment",  "form-comment",  fill_comment),
    #("/products", "form-products", fill_products), SEM ESPAÇO PARA ATTACK
]


# Captura de POSTS do Seleniumwire

# Extrai do request POST os dados relevantes
def extract_post_entry(request) -> dict | None:

    if request.method != "POST":
        return None
    if not request.body:
        return None
    path = urlparse(request.url).path
    try:
        body = request.body.decode("utf-8")
    except Exception:
        return None
    return {
        "class":  "Anomalous",
        "method": "POST",
        "path":   path,
        "params": body,
    }


# Main

def main():
    service = Service(SERVICE_PATH)
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(service=service, options=options)
    wait   = WebDriverWait(driver, 10)

    all_entries = []

    try:
        for repeat in range(REPEATS):
            print(f"\n -- [Rodada] {repeat + 1}/{REPEATS} -- ")

            for url_path, form_id, fill_fn in FORMS:
                full_url = BASE_URL + url_path
                print(f"  [{form_id}] preenchendo...")

                # Limpa requests anteriores do seleniumwire
                del driver.requests

                try:
                    driver.get(full_url)
                    time.sleep(random.uniform(0.5, 1.2))

                    # Preenche o formulário
                    fill_fn(driver, wait)
                    time.sleep(random.uniform(0.3, 0.7))

                    # Submete
                    form = driver.find_element(By.ID, form_id)
                    submit_btn = form.find_element(By.CSS_SELECTOR, "button[type=submit]")
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
                    submit_btn.click()

                    # Aguarda resposta
                    time.sleep(random.uniform(0.5, 1.0))

                    # Captura o POST
                    for req in driver.requests:
                        entry = extract_post_entry(req)
                        if entry and url_path in entry["path"]:
                            all_entries.append(entry)
                            print(f"     capturado: {entry['path']} | {entry['params'][:60]}...")

                except Exception as e:
                    print(f"     erro em {url_path}: {e}")
                    continue

    finally:
        driver.quit()

    # Salva CSV
    print(f"\n[resultado] {len(all_entries)} entradas POST coletadas")

    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["class", "method", "path", "params"],
                                delimiter="«")
        if f.tell() == 0:
            writer.writeheader()
        writer.writerows(all_entries)

    print(f"[csv] salvo em {OUTPUT_CSV}")


if __name__ == "__main__":
    main()