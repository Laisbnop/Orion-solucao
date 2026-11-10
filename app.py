from flask import Flask, jsonify, request
from painel import montar_painel

app = Flask(__name__)

@app.after_request
def liberar_cors(resposta):
    resposta.headers["Access-Control-Allow-Origin"] = "*"
    resposta.headers["Access-Control-Allow-Methods"] = "GET, POST"
    resposta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resposta

@app.route("/")
def home():
    return "Funcionando! Use /login (POST ou GET) com usuario e senha."

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
    app.run(debug=True)
