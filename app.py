"""
==================================================================
APP.PY — Servidor Flask
Fábrica de Projetos | Grupo Orion x CygniAG
==================================================================

ETAPA 3 do roteiro: conectar o processamento de imagem (que já
existia em process_indice.py) numa rota de verdade, pra devolver
o JSON das zonas quando alguém acessar /zonas/<indice>.

COMO TESTAR:
1. No terminal: python3 app.py
2. Abra no navegador: http://localhost:5000/zonas/arvi
   (troca "arvi" pelo nome de qualquer índice que exista na pasta)
3. Deve aparecer um JSON com a lista de zonas (id, row, col,
   avg_score, category, dose_pct)

IMPORTANTE: pra isso funcionar, o process_indice.py precisa estar
na MESMA pasta que este app.py, e o PASTA_ENTRADA dentro dele
precisa apontar pro lugar certo (o mesmo de sempre).
==================================================================
"""

from flask import Flask, jsonify
from process_indice import processar_imagem, aplicar_classificacao, PASTA_ENTRADA
from pathlib import Path

app = Flask(__name__)


@app.route("/")
def home():
    return "Funcionando! Tente acessar /zonas/arvi (ou outro índice) pra ver o JSON."


@app.route("/zonas/<indice>")
def zonas(indice):
    """Processa a imagem do índice pedido e devolve as zonas já
    classificadas, em formato JSON."""

    caminho = Path(PASTA_ENTRADA) / f"{indice}_cloudless_0_100.png"

    if not caminho.exists():
        # tenta a escala min_max como alternativa, caso 0_100 não exista
        caminho = Path(PASTA_ENTRADA) / f"{indice}_cloudless_min_max.png"

    if not caminho.exists():
        return jsonify({"erro": f"Não encontrei imagem para o índice '{indice}'"}), 404

    zonas_calculadas, _img = processar_imagem(caminho)

    if not zonas_calculadas:
        return jsonify({"erro": f"Imagem de '{indice}' não tem dado válido"}), 400

    zonas_calculadas = aplicar_classificacao(zonas_calculadas)

    return jsonify(zonas_calculadas)


if __name__ == "__main__":
    app.run(debug=True)
