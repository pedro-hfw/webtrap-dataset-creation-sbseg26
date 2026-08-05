# WebTrap: Uma Ferramenta de Detecção de Ataques em Requisições HTTP Utilizando Aprendizado de Máquina - Criação do Dataset

Repositório referente ao artigo completo submetido à Trilha Principal do 26º Simpósio Brasileiro de Cibersegurança (SBSEG26).

**Resumo:** Segundo o relatório OWASP Top 10 2025, vulnerabilidades do tipo Injection permanecem entre os principais riscos de segurança para aplicações web. Este trabalho propõe um honeypot web que integra dois modelos de aprendizado de máquina a mecanismos de *deception*. O primeiro modelo identifica requisições HTTP associadas aos ataques SQL Injection, Cross-Site Scripting, Remote Code Execution e Local File Inclusion, distinguindo-as do tráfego benigno, enquanto o segundo classifica a categoria do ataque detectado. Os resultados indicaram taxas de detecção superiores a 94% para tráfego malicioso gerado por ferramentas como sqlmap, XSSER, Commix e Wfuzz. Para requisições benignas, foi obtida uma taxa de acerto de aproximadamente 93%, evidenciando a viabilidade da abordagem proposta para honeypots web inteligentes.

---

# Repositórios

Os artefatos associados ao artigo estão divididos em dois repositórios diferentes, a fim de organização:

- [**webtrap-sbseg26**](https://github.com/pedro-hfw/webtrap-sbseg26): Honeypot web e treinamento de modelos de aprendizado de máquina.
- [**webtrap-dataset-creation-sbseg26**](https://github.com/pedro-hfw/webtrap-dataset-creation-sbseg26): Scripts de geração e coleta de requisições para compor o dataset final.

Este repositório corresponde ao segundo link acima, abordando os códigos de geração e coleta de requisições HTTP, utilizadas para compor o dataset do treinamento dos modelos de aprendizado de máquina do WebTrap.

> ⚠️ AVISO: O repositório principal ([**webtrap-sbseg26**](https://github.com/pedro-hfw/webtrap-sbseg26)) contém a estrutura completa pedida pelo comitê avaliador de artefatos. Considere este repositório como auxiliar, a fim de transparência quanto à criação do dataset mencionado no artigo.

---

# Estrutura do README

Este README está organizado da seguinte forma:

1. [**Título e Resumo**](#webtrap-uma-ferramenta-de-detecção-de-ataques-em-requisições-http-utilizando-aprendizado-de-máquina---criação-do-dataset)
1. [**Dependências**](#dependências)
1. [**Preocupações com Segurança**](#preocupações-com-segurança)
1. [**Estrutura do Repositório**](#estrutura-do-repositório)
1. [**Instalação**](#instalação)
1. [**Execução**](#execução)
1. [**Arquivos de Saída**](#arquivos-de-saída)
1. [**Licença**](#licença)

---

# Dependências

## Hardware

### Geração de Requisições, Selenium e Flask

- Linux (Ubuntu 22.04+, Debian 12+ ou equivalente)
- CPU: mínimo de 4 núcleos (recomendado: 8+)
- RAM: mínimo de 4 GB (recomendado: 8 GB+)
- Espaço em disco: mínimo de 5 GB
- Interface de rede
- Ambiente bare-metal

## Software

- [Git](https://git-scm.com/install/) instalado
- [Python](https://www.python.org/downloads/) 3.12.3+ instalado
- pip
- venv

### Script de Instalação do Git

```bash
sudo apt update
sudo apt install git
```

### Script de Instalação do Python, pip e venv

```bash
sudo apt update
sudo apt install python3-full python3-venv
```

Outras dependências podem ser vistas nos arquivos `requirements-flask.txt` e `requirements-requests.txt`, a saber:

**requirements-flask.txt**

```text
# Framework Web
Flask==3.1.3
Werkzeug==3.1.8
Jinja2==3.1.6
MarkupSafe==3.0.3
itsdangerous==2.2.0
click==8.4.2
blinker==1.9.0
```

**requirements-requests.txt**

```text
# Selenium
selenium==4.46.0
selenium-wire==5.1.0
setuptools==69.5.1

# Dependências do selenium-wire
blinker==1.7.0
brotli==1.2.0
certifi==2026.7.22
cffi==2.1.0
cryptography==38.0.4
h11==0.16.0
h2==4.4.0
hpack==4.2.0
hyperframe==6.1.0
kaitaistruct==0.11
pyasn1==0.6.4
pycparser==3.0
pyOpenSSL==22.1.0
PySocks==1.7.1
zstandard==0.25.0
attrs==26.1.0
outcome==1.3.0.post0
sniffio==1.3.1
sortedcontainers==2.4.0
trio==0.33.0
trio-websocket==0.12.2
wsproto==1.3.2

# Utilitários
idna==3.18
packaging==26.2
pyparsing==3.3.2
typing_extensions==4.16.0
urllib3==2.7.0
websocket-client==1.9.0
```

É possível instalá-las rapidamente como mostrado na seção [Instalação](#instalação).

---

# Preocupações com Segurança

## Porta utilizada

O servidor Flask contendo formulários para geração de requisições POST executa por padrão em:

```
http://127.0.0.1:5000
```

O endereço IP e a porta podem ser modificados utilizando as flags `-e` e `-p`, de acordo com os passos ilustrados na seção de [Execução](#execução).

> ⚠️ Utilizar a flag `-e` expõe a máquina e permite conexão externa dependendo da configuração da máquina e do firewall.

> ⚠️ Algumas portas podem exigir privilégios de administrador. 

---

# Estrutura do Repositório

```
webtrap-dataset-creation-sbseg26/
│
├── payloads.py                         # Dicionário de payloads de ataques e termos benignos
│
├── datasets/                           # Datasets finais usados no treinamento dos modelos
│   ├── dataset_attack_classifier.csv
│   └── dataset_request_classifier.csv
│
├── generated_requests/                 # Pasta contendo CSVs das requisições geradas pelos scripts (ignorada pelo git)
│
├── top-usernames-shortlist.txt         # Lista de usernames, autoria das SecLists
├── rockyou.txt                         # Lista de senhas (download separado), autoria das SecLists
│
├── valid_search_gets.py                # Geração de GET válidos (busca)
├── valid_login_posts.py                # Geração de POST válidos (login)
├── valid_forum_gets.py                 # Geração de GET válidos (fórum)
├── anomalous_search_gets.py            # Geração de GET maliciosos (busca)
├── anomalous_login_posts.py            # Geração de POST maliciosos (login)
├── anomalous_forum_gets.py             # Geração de GET maliciosos (fórum)
│
└── selenium/                           # Geradores e coleta de requisições usando Selenium
    ├── payloads.py                     # Cópia do payloads.py do diretório raiz
    ├── valid_selenium_navigator.py     # Navegação em sites e coleta de requisições GET válidas
    ├── valid_selenium_flask.py         # Navegação no Flask local para geração de POSTS válidos
    ├── anomalous_selenium_flask.py     # Navegação no Flask local para geração de POSTS maliciosos
    └── flask_server/                    
        ├── app.py                      # Servidor Flask com página web contendo diversos formulários, usado em conjunto com *_selenium_flask.py
        └── templates/                  # Templates HTML
```

---

# Instalação

⚠️ **ATENÇÃO:** Para garantir a reprodutibilidade dos códigos, faça a instalação do repositório na máquina host (ambiente bare-metal). A conexão entre Firefox e Geckodriver (para os scripts com Selenium) demonstrou problemas na execução dos testes em máquinas virtuais. 

### 1. Clone o repositório e entre em seu diretório

```bash
git clone https://github.com/pedro-hfw/webtrap-dataset-creation-sbseg26.git

cd webtrap-dataset-creation-sbseg26
```

### 2. Crie dois ambientes virtuais e instale as dependências

É preciso utilizar ambientes virtuais separados para o Flask e para o Selenium, devido a conflitos de versão da biblioteca *Blinker*.

```bash
python3 -m venv venv-flask

source venv-flask/bin/activate

pip install -r requirements-flask.txt
```

> **Nota**: Antes de criar o segundo ambiente virtual, saia do anterior com `deactivate`.

```bash
python3 -m venv venv-requests

source venv-requests/bin/activate

pip install -r requirements-requests.txt
```

### 3. Download do `rockyou.txt` (requerido para geradores de login)

O `rockyou.txt` é uma lista de palavras de ~133 MB e não está incluída no repositório.

Para fazer sua instalação, siga as instruções em https://github.com/danielmiessler/SecLists ou o passo a passo abaixo:

#### 1. Clone das SecLists:

```bash
git clone --depth 1 https://github.com/danielmiessler/SecLists.git
```

A clonagem pode demorar alguns minutos.

#### 2. Descompactar e mover o `rockyou.txt` para o repositório:

```bash
cd SecLists/Passwords/Leaked-Databases

tar -xvzf rockyou.txt.tar.gz

# Exemplo - altere o caminho conforme necessário
cp rockyou.txt /home/{SEU_USUARIO}/webtrap-dataset-creation-sbseg26
```

No final, é necessário que `rockyou.txt` esteja na mesma pasta que os geradores `valid_login_posts.py` e `anomalous_login_posts.py`.

### 4. Instale o Geckodriver (para Selenium)

Instale de acordo com sua preferência via apt ou manualmente no GitHub (recomendado), escolhendo a versão correspondente ao seu Linux.

Os códigos foram executados utilizando a versão 0.37.1 do geckodriver e 153.0.1 do firefox.

Instalação no GitHub: https://github.com/mozilla/geckodriver/releases

> **Nota**: O arquivo de instalação pode aparecer no diretório `Downloads`, execute os comandos nele se necessário.

Após a instalação manual, siga os passos:

#### 1. Descompacte e dê permissão de execução:

```bash
tar -xvzf geckodriver-v0.37.1-linux64.tar.gz

chmod +x geckodriver
```

#### 2. Mova-o para o diretório de binários:

```bash
sudo mv geckodriver /usr/local/bin/
```

#### 3. Verificando a instalação:

```bash
geckodriver --version
```

É esperado um output da forma:

```bash
geckodriver 0.37.1 (300705c65d1b 2026-07-17 09:25 +0000)
```

---

# Execução

Todas as requisições geradas são salvas em arquivos CSV na pasta `generated_requests/`.
Cada script gera um arquivo com seu nome correspondente, e não apaga o conteúdo do arquivo CSV entre execuções.

Abaixo está listado como executar cada script:

### Geradores de Requisições HTTP

#### 1. Navegue ao diretório e ative o ambiente virtual das requisições:

```bash
cd webtrap-dataset-creation-sbseg26

source venv-requests/bin/activate
```

#### 2. Execute os geradores:

Cada gerador aceita as seguintes flags:
- `-r`: Quantidade de requisições geradas (padrão 3000);
- `-s`: **Exclusiva para maliciosos** — codifica o payload uma única vez;
- `-d`: **Exclusiva para maliciosos** — codifica o payload duas vezes (double-encoding);

Exemplos de execução:

**Benigno**

```bash
python3 valid_search_gets.py -r 3000
```
```bash
python3 valid_login_posts.py -r 1000
```
```bash
python3 valid_forum_gets.py  -r 3000
```

**Malicioso (payload padrão: SQLI_TERMS)**

```bash
python3 anomalous_search_gets.py -r 3000
```
```bash
python3 anomalous_search_gets.py -r 3000 -s
```
```bash
python3 anomalous_search_gets.py -r 3000 -d
```

```bash
python3 anomalous_login_posts.py -r 1000
```
```bash
python3 anomalous_forum_gets.py  -r 3000
```

> **Nota:** Para trocar o tipo de payload (ex: XSS, RCE, LFI), edite a constante `PAYLOAD` nos arquivos geradores de tráfego malicioso para um dos tipos presente em `payloads.py`.

Também é possível alterar a estrutura das requisições geradas (como omitir um parâmetro) editando os códigos geradores, a fim de gerar maior diversidade.

### Selenium - Navegação Web (Requisições GET legítimas)

Captura de requisições legítimas navegando em um site escolhido para coletar URLs com parâmetros.

> **Nota:** Nem todos os sites possuem URLs com parâmetros de consulta (queries), que são as requisições procuradas.

#### 1. Navegue ao diretório e ative o ambiente virtual das requisições:

```bash
cd webtrap-dataset-creation-sbseg26

source venv-requests/bin/activate
```

#### 2. Entre no diretório do Selenium e execute o código:

> ⚠️ É necessário alterar o site escolhido para navegar pelas constantes SITE e INITIAL_URL no topo do script `valid_selenium_navigator.py`. O código também aceita a flag `-r` para quantidade de repetições (padrão 10).

```bash
cd selenium

# Edite SITE e INITIAL_URL no topo do script, depois:
python3 valid_selenium_navigator.py -r 20
```

Serão impressas informações durante a execução do código, a fim de verificar se está funcionando corretamente.

As requisições capturadas poderão ser encontradas em `generated_requests`.

### Selenium - Submissão de Formulários com Flask

Será necessário utilizar dois terminais para executar o código. 

#### 1. Em um primeiro terminal, entre no diretório e ative o ambiente virtual do Flask:

```bash
cd webtrap-dataset-creation-sbseg26

source venv-flask/bin/activate

cd selenium/flask_server
```

#### 2. Inicie o servidor Flask:

Exemplos:

```bash
# atuando em 127.0.0.1:5000 por padrão
python3 app.py
```
```bash
# exposição em 0.0.0.0 (permite acesso externo)
python3 app.py -e
```
```bash
# usando outra porta
python3 app.py -p 8080   
```

> É possível utilizar as flags `-e` para expor o Flask na rede ou `-p` para alterar a porta.

#### Extra: Executando em Porta Privilegiada com SUDO

Caso queira executar o servidor Flask em uma porta que exige permissão de superusuário (portas abaixo de 1024, como a 80 ou 443), siga os passos abaixo:

```bash
sudo -i

# Navegue até o diretório do repositório
cd /home/{SEU_USUARIO}/webtrap-dataset-creation-sbseg26

# Ative o ambiente virtual do Flask
source venv-flask/bin/activate

# Navegue até o diretório do Flask
cd selenium/flask_server

# Substitua {PORTA} pela porta desejada
python3 app.py -p {PORTA}
```

#### 3. No segundo terminal, entre no diretório e ative o ambiente virtual das requisições:

```bash
cd webtrap-dataset-creation-sbseg26

source venv-requests/bin/activate

cd selenium
```

#### 4. Execute o código:

```bash
# Para tráfego benigno
python3 valid_selenium_flask.py -r 10
```
```bash
# Para tráfego malicioso (padrão: SQLI_TERMS)
python3 anomalous_selenium_flask.py -r 20
```

> **Nota:** Para trocar o tipo de payload (ex: XSS, RCE, LFI), edite a constante `PAYLOAD` nos arquivos geradores de tráfego malicioso para um dos tipos presente em `payloads.py`.

Os dois códigos acima permitem alterar a quantidade de execuções com a flag `-r` (padrão 10).

As requisições geradas poderão ser encontradas em `generated_requests`.

---

# Arquivos de Saída

Todos os arquivos CSV contendo as requisições geradas ou coletadas estão em `generated_requests`.

Esses arquivos possuem `«` como delimitador para não ter conflito com caracteres especiais dos payloads.

Os arquivos de geração de requisições sem selenium produzem CSVs com os campos: `class`, `method` e `params`.

Já os geradores com selenium também geram CSVs com as mesmas colunas com a adição da coluna `path`, a fim de facilitar futuras melhorias aos modelos.

É possível unir esses arquivos copiando as informações uns dos outros e colando em um arquivo final, sendo que no caso das requisições com selenium será necessário remover a coluna `path`, que pode ser feito utilizando diversas ferramentas na internet (como o Power Query do Microsoft Excel).

---

# Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais informações.