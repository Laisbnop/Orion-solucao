"""
==================================================================
LEITOR DO CONTORNO DO TALHÃO (KML)
Fábrica de Projetos | Grupo Orion x CygniAG
==================================================================

O QUE ISSO FAZ:
Lê o arquivo contorno_kml (o contorno real do talhão, com
coordenadas de latitude/longitude) e devolve uma lista de pontos
prontos pra desenhar num mapa (Leaflet, Google Maps, etc).

Isso é a peça que faltava pra ligar o processamento de imagem
(zonas) com um mapa de verdade — antes a gente só tinha isso "preso"
dentro do HTML da demo; agora vira uma função reutilizável.

ONDE ISSO ENTRA NO FLUXO GERAL:
  1. processar_imagem()       -> zonas (Laís)
  2. aplicar_classificacao()  -> categoria + dose (Letícia)
  3. ler_contorno_talhao()    -> coordenadas do talhão  <- ESTE ARQUIVO
  4. Front-end junta os dois (zonas + contorno) no mapa
==================================================================
"""

import re


def ler_contorno_talhao(caminho_kml):
    """Lê um arquivo .kml e devolve o contorno do talhão como uma
    lista de pontos [lat, lon] (nessa ordem, porque é o que o
    Leaflet espera).

    Exemplo de uso:
        pontos = ler_contorno_talhao("contorno_kml")
        pontos[0]  ->  [-22.714006532072, -55.544751311567]
    """
    with open(caminho_kml, encoding="utf-8") as f:
        conteudo = f.read()

    match = re.search(r"<coordinates>(.*?)</coordinates>", conteudo, re.DOTALL)
    if not match:
        raise ValueError("Não encontrei nenhuma tag <coordinates> nesse KML.")

    texto_coordenadas = match.group(1).strip()

    pontos = []
    for token in texto_coordenadas.split():
        # cada token do KML vem como "longitude,latitude,altitude"
        lon, lat, _altitude = token.split(",")
        pontos.append([float(lat), float(lon)])  # Leaflet quer [lat, lon]

    return pontos


def calcular_caixa_delimitadora(pontos):
    """Dado o contorno (lista de [lat, lon]), devolve os limites
    (bounding box) — útil pra posicionar a grade de zonas dentro do
    talhão, do mesmo jeito que fizemos na demo."""
    lats = [p[0] for p in pontos]
    lons = [p[1] for p in pontos]
    return {
        "lat_min": min(lats),
        "lat_max": max(lats),
        "lon_min": min(lons),
        "lon_max": max(lons),
    }


if __name__ == "__main__":
    # teste rápido: rode "python3 ler_contorno.py" com o contorno_kml
    # na mesma pasta pra conferir se está lendo certo
    pontos = ler_contorno_talhao("contorno_kml")
    print(f"{len(pontos)} pontos encontrados no contorno.")
    print("Primeiro ponto:", pontos[0])
    print("Caixa delimitadora:", calcular_caixa_delimitadora(pontos))
