"""
==================================================================
APP.PY — Esqueleto do servidor Flask
Fábrica de Projetos | Grupo Orion x CygniAG
==================================================================

ETAPA 2 do roteiro: só provar que o Flask está funcionando, antes
de conectar qualquer processamento de imagem. Não faz nada além
disso ainda — de propósito, pra testarmos uma coisa de cada vez.

COMO TESTAR:
1. No terminal: python3 app.py
2. Abra no navegador: http://localhost:5000
3. Se aparecer a mensagem "Funcionando! ..." está tudo certo.
4. Pra parar o servidor: Ctrl+C no terminal
==================================================================
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Funcionando! O servidor Flask está de pé. Próxima etapa: conectar o processamento."


if __name__ == "__main__":
    app.run(debug=True)
