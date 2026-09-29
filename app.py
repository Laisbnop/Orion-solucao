"""
==================================================================
APP.PY — Servidor Flask final
Fábrica de Projetos | Grupo Orion x CygniAG
==================================================================

O QUE ISSO FAZ:
Expõe uma rota /login que o index.html vai chamar. Essa rota usa
a função montar_painel, que já existe em painel.py e já junta
tudo: login, permissão, desvio e motivo do clima.

Ou seja: este arquivo não tem lógica nova nenhuma — ele só "abre
uma porta na internet" para o que vocês já construíram.

COMO TESTAR (sem o HTML ainda):
1. No terminal: python3 app.py
2. Deve aparecer: * Running on http://127.0.0.1:5000
3. Com o servidor rodando, teste com o navegador acessando:
   http://localhost:5000/login?usuario=produtor1&senha=santaluzia123
   (isso simula um login GET só pra teste rápido; o index.html vai
   usar POST de verdade)
==================================================================
"""

from flask import Flask, jsonify, request
from painel import montar_painel

app = Flask(__name__)


@app.after_request
def liberar_cors(resposta):
    """Sem isso, o navegador bloqueia a chamada quando o HTML é
    aberto direto como arquivo (file://) tentando falar com o
    Flask (localhost:5000) — são "origens" diferentes pro
    navegador. Como isso é um protótipo local, liberamos geral."""
    resposta.headers["Access-Control-Allow-Origin"] = "*"
    resposta.headers["Access-Control-Allow-Methods"] = "GET, POST"
    resposta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resposta


@app.route("/")
def home():
    return "Funcionando! Use /login (POST) com usuario e senha."


@app.route("/login", methods=["GET", "POST"])
def login():
    """Recebe usuário e senha (via POST, formato JSON, vindo do
    index.html — mas também aceita GET com parâmetros na URL,
    só pra facilitar testes rápidos no navegador) e devolve o
    resultado completo de montar_painel()."""

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
