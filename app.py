"""
==================================================================
APP.PY — Servidor Flask
Fábrica de Projetos | Grupo Orion x CygniAG
==================================================================

ETAPA 4 do roteiro: rota de upload. Agora a pessoa pode escolher
QUALQUER imagem do computador dela, em vez do sistema só ler um
arquivo fixo que já estava na pasta.

COMO TESTAR (sem interface ainda, só a rota):
1. No terminal: python3 app.py
2. Abra no navegador: http://localhost:5000/upload
   -> deve aparecer um formulário simples de upload
3. Escolha uma imagem de índice (tipo arvi_cloudless_0_100.png)
   e clique em enviar
4. Deve aparecer o JSON com as zonas calculadas NA HORA, a partir
   do arquivo que você escolheu — não mais de um arquivo fixo

IMPORTANTE: pra isso funcionar, o process_indice.py precisa estar
na MESMA pasta que este app.py.
==================================================================
"""

from flask import Flask, jsonify, request
from process_indice import processar_imagem, aplicar_classificacao, PASTA_ENTRADA
from pathlib import Path

app = Flask(__name__)

PASTA_TEMPORARIA = Path("uploads_temp")
PASTA_TEMPORARIA.mkdir(exist_ok=True)


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


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """GET: mostra um formulário simples de upload (só pra testar
    pelo navegador, sem precisar de interface bonita ainda).

    POST: recebe o arquivo enviado, salva numa pasta temporária,
    processa e devolve o JSON das zonas — igual a rota /zonas/,
    mas com um arquivo que a pessoa escolheu, não um fixo."""

    if request.method == "GET":
        return """
        <h3>Upload de imagem de índice</h3>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="imagem" accept=".png">
            <button type="submit">Enviar</button>
        </form>
        """

    # a partir daqui é o POST: o arquivo já foi enviado

    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhum arquivo foi enviado"}), 400

    arquivo = request.files["imagem"]

    if arquivo.filename == "":
        return jsonify({"erro": "Nenhum arquivo foi selecionado"}), 400

    if not arquivo.filename.lower().endswith(".png"):
        return jsonify({"erro": "Só aceito arquivos .png por enquanto"}), 400

    # salva numa pasta temporária, com o nome original do arquivo
    caminho_salvo = PASTA_TEMPORARIA / arquivo.filename
    arquivo.save(caminho_salvo)

    # processa exatamente como já fazíamos na rota /zonas/<indice>
    zonas_calculadas, _img = processar_imagem(caminho_salvo)

    if not zonas_calculadas:
        return jsonify({"erro": "Essa imagem não tem dado válido (talvez esteja vazia ou seja um dia nublado)"}), 400

    zonas_calculadas = aplicar_classificacao(zonas_calculadas)

    return jsonify(zonas_calculadas)


if __name__ == "__main__":
    app.run(debug=True)
