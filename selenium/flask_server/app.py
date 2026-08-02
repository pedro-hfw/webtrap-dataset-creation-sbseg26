from flask import Flask, request, render_template, jsonify
from datetime import datetime
import argparse

# -----------------------
# Parsing de argumentos
# -----------------------

parser = argparse.ArgumentParser(description = "Flask para Requisições POST")

parser.add_argument(
    "-e", "--expose", 
    action="store_true", 
    help="Alterna o IP para acesso externo"
)

parser.add_argument(
    "-p","--port",
    type=int,
    default=5000,
    help="Alterna a porta utilizada"
)

args = parser.parse_args()

HOST_IP = "0.0.0.0" if args.expose else "127.0.0.1"
HOST_PORT = args.port


# -----------------------
# Configuração do Flask
# -----------------------


app = Flask(__name__)

# Log de Requisições recebidas (debug)
received_requests = []

def log_request(form_type: str, data: dict):
    received_requests.append({
        "timestamp": datetime.now().isoformat(),
        "form_type": form_type,
        "data": data,
    })


# Página Principal
@app.route("/")
def index():
    return render_template("index.html")


# Formulário 1 - Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        log_request("login", dict(request.form))
        return jsonify({"status": "ok", "form": "login", "received": dict(request.form)})
    return render_template("login.html")


# Formulário 2 - Cadastro de usuário
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        log_request("register", dict(request.form))
        return jsonify({"status": "ok", "form": "register", "received": dict(request.form)})
    return render_template("register.html")


# Formulário 3 - Busca com filtros
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        log_request("search", dict(request.form))
        return jsonify({"status": "ok", "form": "search", "received": dict(request.form)})
    return render_template("search.html")


# Formulário 4 - Comentário / contato
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        log_request("contact", dict(request.form))
        return jsonify({"status": "ok", "form": "contact", "received": dict(request.form)})
    return render_template("contact.html")


# Formulário 5 - Perfil de usuário (update)
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        log_request("profile", dict(request.form))
        return jsonify({"status": "ok", "form": "profile", "received": dict(request.form)})
    return render_template("profile.html")


# Formulário 6 - Pedido / checkout simples
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        log_request("checkout", dict(request.form))
        return jsonify({"status": "ok", "form": "checkout", "received": dict(request.form)})
    return render_template("checkout.html")


# Formulário 7 - Comentário em post/artigo
@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        log_request("comment", dict(request.form))
        return jsonify({"status": "ok", "form": "comment", "received": dict(request.form)})
    return render_template("comment.html")



# Formulário 8 - Filtro de produtos
@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "POST":
        log_request("products", dict(request.form))
        return jsonify({"status": "ok", "form": "products", "received": dict(request.form)})
    return render_template("products.html")


# Endpoint de debug
@app.route("/debug/requests")
def debug_requests():
    return jsonify(received_requests)


if __name__ == "__main__":
    app.run(host=HOST_IP, debug=True, port=HOST_PORT)
