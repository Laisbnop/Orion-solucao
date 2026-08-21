"""
==================================================================
PROTÓTIPO — Zoneamento de aplicação a partir de MÚLTIPLOS índices
Fábrica de Projetos | Grupo Orion x CygniAG
==================================================================

ESTE ARQUIVO É UMA EVOLUÇÃO DO "process_arvi.py".
A lógica de dentro (ler pixel, calcular score, classificar zona,
sugerir dose) é EXATAMENTE A MESMA. A única coisa nova aqui é que,
em vez de vocês apontarem pra UM arquivo (arvi_cloudless_0_100.png),
o script agora VARRE A PASTA INTEIRA sozinho, descobre quais
índices existem (arvi, evi, gci, ndmi, ndre, ndvi, osavi...) e
processa cada um automaticamente.

Ou seja: isso resolve o "tenho muita imagem e não sei por onde
começar" — mas não substitui vocês entenderem o que cada índice
significa nem decidirem como usar isso na interface. Isso continua
sendo trabalho do grupo.

--------------------------------------------------------------
SOBRE OS NOMES DOS ARQUIVOS QUE VOCÊS TÊM
--------------------------------------------------------------
Pelo padrão que apareceu na pasta de vocês, cada índice gera:

  {indice}_cloudless_0_100.png     -> imagem em escala 0-100
  {indice}_cloudless_min_max.png   -> imagem em escala min-max
  {indice}_cloudless_std_25.png    -> outra variação de escala
  {indice}_cloudless_std_35.png    -> outra variação de escala
  {indice}_cloudy_*.png            -> normalmente vazias (678 bytes),
                                       provavelmente dias sem imagem
                                       válida por causa de nuvem —
                                       o script ignora essas
  {indice}_cut.tif                 -> recorte do talhão (não usado ainda)
  cmask.tif                        -> máscara de nuvem (não usado ainda)

--------------------------------------------------------------
O QUE CADA ÍNDICE SIGNIFICA (resumo rápido pra vocês entenderem
o que estão mostrando, útil pra justificativa/pitch do projeto):
--------------------------------------------------------------
  NDVI  -> vigor/verde geral da vegetação (o mais clássico)
  ARVI  -> parecido com o NDVI, mas mais resistente a interferência
           atmosférica (neblina, poeira)
  EVI   -> parecido com NDVI, mas funciona melhor quando a vegetação
           é muito densa (onde o NDVI "satura")
  GCI   -> relacionado à quantidade de clorofila (nutrição da planta)
  NDRE  -> sensível a estresse/nitrogênio em estágios mais avançados
           da cultura
  NDMI  -> relacionado à umidade da vegetação (não é bem "verde",
           é "água")
  OSAVI -> parecido com NDVI, mas ajustado pra funcionar melhor
           quando a planta ainda é pequena / solo aparece muito

  Repara que nem todos medem "a mesma coisa" — por isso pode fazer
  sentido, no futuro, combinar mais de um índice na recomendação
  (tem uma função opcional pra isso no fim do arquivo).
==================================================================
"""

import json
import re
from pathlib import Path
from PIL import Image


# ==================================================================
# CONFIGURAÇÃO — mexam aqui
# ==================================================================
PASTA_ENTRADA = "/Users/lais/Desktop/projeto-orion-cygnia/sentinel-21"          # pasta onde estão os PNGs baixados
PASTA_SAIDA = "saida"        # pasta onde os resultados vão ser salvos
ESCALA_PADRAO = "0_100"      # qual variação de escala usar por padrão
CELL_SIZE = 15               # tamanho de cada zona, em pixels

# tamanho mínimo (em bytes) pra considerar que a imagem tem dado de
# verdade. Os arquivos "cloudy_*" que vocês têm ficam com ~678 bytes
# (praticamente vazios) — o script pula esses automaticamente.
TAMANHO_MINIMO_VALIDO = 1000


# ==================================================================
# PARTE 1 — LAÍS (leitura da imagem / processamento)
# (idêntico ao process_arvi.py, só copiado pra cá)
# ==================================================================

def carregar_imagem(caminho):
    img = Image.open(caminho).convert("RGBA")
    return img, img.size


def calcular_score_pixel(r, g, b, a, g_min, g_max):
    if a == 0:
        return None
    if g_max == g_min:
        return 50.0
    return (g - g_min) / (g_max - g_min) * 100


def processar_imagem(caminho, cell_size=CELL_SIZE):
    img, (largura, altura) = carregar_imagem(caminho)
    px = img.load()

    valores_verde = [
        px[x, y][1]
        for x in range(largura)
        for y in range(altura)
        if px[x, y][3] > 0
    ]
    if not valores_verde:
        return [], img  # imagem sem nenhum pixel de talhão válido

    g_min, g_max = min(valores_verde), max(valores_verde)

    zonas = []
    zone_id = 1
    linhas = (altura + cell_size - 1) // cell_size
    colunas = (largura + cell_size - 1) // cell_size

    for row in range(linhas):
        for col in range(colunas):
            x0, y0 = col * cell_size, row * cell_size
            x1, y1 = min(x0 + cell_size, largura), min(y0 + cell_size, altura)

            scores_da_zona = []
            for x in range(x0, x1):
                for y in range(y0, y1):
                    r, g, b, a = px[x, y]
                    score = calcular_score_pixel(r, g, b, a, g_min, g_max)
                    if score is not None:
                        scores_da_zona.append(score)

            if not scores_da_zona:
                continue

            media = sum(scores_da_zona) / len(scores_da_zona)
            zonas.append({
                "id": zone_id,
                "row": row,
                "col": col,
                "avg_score": round(media, 1),
            })
            zone_id += 1

    return zonas, img


# ==================================================================
# PARTE 2 — LETÍCIA (classificação + regra de dose)
# (idêntico ao process_arvi.py, só copiado pra cá)
# ==================================================================

def classificar_zona(avg_score):
    if avg_score < 33:
        return "Baixa"
    elif avg_score < 66:
        return "Média"
    else:
        return "Alta"


def dose_recomendada(categoria):
    doses = {"Baixa": 115, "Média": 100, "Alta": 85}
    return doses[categoria]


def aplicar_classificacao(zonas):
    for zona in zonas:
        categoria = classificar_zona(zona["avg_score"])
        zona["category"] = categoria
        zona["dose_pct"] = dose_recomendada(categoria)
    return zonas


def gerar_mapa_de_zonas(img, zonas, cell_size=CELL_SIZE):
    cores = {"Baixa": (214, 69, 65), "Média": (232, 168, 56), "Alta": (58, 143, 92)}
    largura, altura = img.size
    px = img.load()
    overlay = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    overlay_px = overlay.load()

    for zona in zonas:
        x0, y0 = zona["col"] * cell_size, zona["row"] * cell_size
        x1 = min(x0 + cell_size, largura)
        y1 = min(y0 + cell_size, altura)
        cor = cores[zona["category"]]
        for x in range(x0, x1):
            for y in range(y0, y1):
                if px[x, y][3] > 0:
                    overlay_px[x, y] = (*cor, 235)

    return overlay


# ==================================================================
# PARTE 3 — NOVIDADE: descoberta automática dos índices na pasta
# ==================================================================
# Essa é a parte que resolve o "tenho muita imagem". Em vez de
# escrever "arvi_cloudless_0_100.png" na mão, a gente escaneia a
# pasta e descobre sozinho quais índices existem.

PADRAO_ARQUIVO = re.compile(r"^([a-z0-9]+)_cloudless_(.+)\.png$")


def descobrir_indices(pasta):
    """Olha os arquivos da pasta e devolve um dicionário assim:
       { "arvi": ["0_100", "min_max", "std_25", "std_35"],
         "ndvi": ["0_100", "min_max", ...], ... }
    """
    pasta = Path(pasta)
    indices = {}

    for arquivo in pasta.glob("*_cloudless_*.png"):
        m = PADRAO_ARQUIVO.match(arquivo.name)
        if not m:
            continue
        indice, escala = m.group(1), m.group(2)

        # pula arquivos "vazios" (placeholder de dia nublado, por
        # exemplo) usando o tamanho do arquivo como sinal
        if arquivo.stat().st_size < TAMANHO_MINIMO_VALIDO:
            continue

        indices.setdefault(indice, []).append(escala)

    return indices


# ==================================================================
# EXECUÇÃO EM LOTE — processa todos os índices encontrados
# ==================================================================

def processar_pasta(pasta_entrada=PASTA_ENTRADA, pasta_saida=PASTA_SAIDA,
                     escala=ESCALA_PADRAO):
    pasta_entrada = Path(pasta_entrada)
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(exist_ok=True)

    indices_encontrados = descobrir_indices(pasta_entrada)

    if not indices_encontrados:
        print("Nenhum índice encontrado nessa pasta. Confira o PASTA_ENTRADA.")
        return {}

    print(f"Índices encontrados: {sorted(indices_encontrados.keys())}\n")

    resultados = {}

    for indice, escalas_disponiveis in sorted(indices_encontrados.items()):
        escala_usar = escala if escala in escalas_disponiveis else escalas_disponiveis[0]
        nome_arquivo = f"{indice}_cloudless_{escala_usar}.png"
        caminho = pasta_entrada / nome_arquivo

        zonas, img = processar_imagem(caminho)
        if not zonas:
            print(f"  [{indice}] pulado — imagem sem dado válido")
            continue

        zonas = aplicar_classificacao(zonas)
        mapa_zonas = gerar_mapa_de_zonas(img, zonas)

        mapa_zonas.save(pasta_saida / f"{indice}_zonas.png")
        with open(pasta_saida / f"{indice}_zonas.json", "w", encoding="utf-8") as f:
            json.dump(zonas, f, ensure_ascii=False, indent=2)

        resultados[indice] = zonas
        print(f"  [{indice}] escala usada: {escala_usar} -> {len(zonas)} zonas")

    return resultados


# ==================================================================
# BÔNUS (opcional) — combinar vários índices numa recomendação única
# ==================================================================
# Ideia: já que cada índice mede uma coisa um pouco diferente
# (vigor, clorofila, umidade...), dá pra combinar mais de um pra
# ter uma recomendação mais robusta que usar só um índice sozinho.
# Isso é OPCIONAL — só usem se quiserem deixar o projeto mais
# sofisticado. Combina a média de score das mesmas zonas (row, col)
# entre os índices escolhidos.

def combinar_indices(resultados, indices_para_combinar):
    """resultados: o dicionário devolvido por processar_pasta()
       indices_para_combinar: lista de nomes, ex: ["ndvi", "ndre", "ndmi"]
    """
    mapas = {nome: {(z["row"], z["col"]): z["avg_score"]
                     for z in resultados[nome]}
             for nome in indices_para_combinar if nome in resultados}

    if not mapas:
        return []

    todas_posicoes = set()
    for mapa in mapas.values():
        todas_posicoes.update(mapa.keys())

    combinado = []
    zone_id = 1
    for (row, col) in sorted(todas_posicoes):
        scores = [mapa[(row, col)] for mapa in mapas.values() if (row, col) in mapa]
        if not scores:
            continue
        media = sum(scores) / len(scores)
        categoria = classificar_zona(media)
        combinado.append({
            "id": zone_id,
            "row": row,
            "col": col,
            "avg_score": round(media, 1),
            "category": categoria,
            "dose_pct": dose_recomendada(categoria),
            "indices_usados": list(mapas.keys()),
        })
        zone_id += 1

    return combinado


# ==================================================================
# EXECUÇÃO
# ==================================================================

if __name__ == "__main__":
    resultados = processar_pasta()

    # exemplo de uso do bônus (só roda se tiver os índices citados):
    # combinado = combinar_indices(resultados, ["ndvi", "ndre", "ndmi"])
    # with open("saida/combinado_zonas.json", "w", encoding="utf-8") as f:
    #     json.dump(combinado, f, ensure_ascii=False, indent=2)
