import os
from flask import Flask, jsonify, request, send_from_directory
from painel import montar_painel

app = Flask(__name__, static_folder=".", static_url_path="")

@app.after_request
def liberar_cors(resposta):
    resposta.headers["Access-Control-Allow-Origin"] = "*"
    resposta.headers["Access-Control-Allow-Methods"] = "GET, POST"
    resposta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resposta

@app.route("/")
def home():
    # Serve o próprio dashboard na raiz, assim o link direto já abre a tela de login.
    return send_from_directory(".", "dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        dados = request.get_json(silent=True) or {}
        usuario = dados.get("usuario", "")
        senha = dados.get("senha", "")
    else:
        usuario = request.args.get("usuario", "")
        senha = request.args.get("senha", "")

    if not usuario or not senha:
        return jsonify({"sucesso": False, "motivo": "Usuário e senha são obrigatórios"}), 400

    resultado = montar_painel(usuario, senha)
    if not resultado["sucesso"]:
        return jsonify(resultado), 401
    return jsonify(resultado)

if __name__ == "__main__":
    # Em produção (Render), a porta vem da variável de ambiente PORT.
    # Localmente, continua rodando em 5000 como antes.
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta, debug=False)
