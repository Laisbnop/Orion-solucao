"""
 a lógica tem duas camadas:
  1. Causa mecânica (sempre sugerida, quando há desvio) — o texto
     muda dependendo se o desvio foi pra menos ou pra mais
  2. Fator climático adicional (só aparece se, além do desvio,
     choveu bastante naquele dia) — não substitui a causa mecânica,
     só soma a ela

REGRA:
  - status == "Dentro do esperado" -> não avalia nada
  - status == "Abaixo do esperado" -> causa mecânica de subaplicação
  - status == "Acima do esperado"  -> causa mecânica de superaplicação
  - em qualquer um dos dois casos acima, se chuva_mm >= 10 no dia,
    soma um fator climático adicional ao texto
==================================================================
"""


CHUVA_RELEVANTE_MM = 10

CLIMA_FICTICIO = {
    "2026-08-12": {"chuva_mm": 0.0,  "temp_media": 24.1},
    "2026-08-13": {"chuva_mm": 0.0,  "temp_media": 25.3},
    "2026-08-14": {"chuva_mm": 3.2,  "temp_media": 23.8},
    "2026-08-15": {"chuva_mm": 0.0,  "temp_media": 26.0},
    "2026-08-16": {"chuva_mm": 22.5, "temp_media": 21.4},
    "2026-08-17": {"chuva_mm": 0.0,  "temp_media": 27.1},
    "2026-08-18": {"chuva_mm": 18.7, "temp_media": 22.0},
    "2026-08-19": {"chuva_mm": 0.0,  "temp_media": 25.9},
    "2026-08-20": {"chuva_mm": 0.0,  "temp_media": 26.4},
    "2026-08-21": {"chuva_mm": 15.3, "temp_media": 22.8},
    "2026-08-22": {"chuva_mm": 0.0,  "temp_media": 27.5},
    "2026-08-23": {"chuva_mm": 0.0,  "temp_media": 28.0},
    "2026-08-24": {"chuva_mm": 4.1,  "temp_media": 24.3},
    "2026-08-25": {"chuva_mm": 0.0,  "temp_media": 26.7},
    "2026-08-26": {"chuva_mm": 0.0,  "temp_media": 25.5},
    "2026-08-27": {"chuva_mm": 0.0,  "temp_media": 26.9},
    "2026-08-28": {"chuva_mm": 0.0,  "temp_media": 27.2},
    "2026-08-29": {"chuva_mm": 12.4, "temp_media": 23.1},
    "2026-08-30": {"chuva_mm": 0.0,  "temp_media": 25.0},
    "2026-08-31": {"chuva_mm": 31.8, "temp_media": 20.6},
}

# Textos de causa mecânica, variando conforme a direção do desvio
CAUSA_MECANICA_ABAIXO = "Possível causa mecânica — verificar entupimento ou desgaste do bico"
CAUSA_MECANICA_ACIMA = "Possível causa mecânica — verificar calibração da válvula ou pressão da bomba"


def motivo_provavel(data, status):
    """Função principal: recebe a data da aplicação e o status do
    desvio (vindo do comparacao.py), e devolve um dicionário com o
    motivo provável — priorizando causa mecânica, com o clima como
    fator adicional quando relevante."""

    if status == "Dentro do esperado":
        return {"texto": "—", "tipo": "neutro"}

    # 1. Causa mecânica, sempre sugerida quando há desvio
    if status == "Abaixo do esperado":
        texto = CAUSA_MECANICA_ABAIXO
    else:  # "Acima do esperado"
        texto = CAUSA_MECANICA_ACIMA

    # 2. Fator climático adicional, só quando choveu bastante naquele dia
    clima_do_dia = CLIMA_FICTICIO.get(data)
    if clima_do_dia is not None and clima_do_dia["chuva_mm"] >= CHUVA_RELEVANTE_MM:
        texto += f". Fator adicional: chuva de {clima_do_dia['chuva_mm']}mm registrada no dia"

    return {"texto": texto, "tipo": "mecanica"}


# ==================================================================
# TESTES
# ==================================================================

if __name__ == "__main__":
    casos_de_teste = [
        {"talhao": "T02", "data": "2026-08-13", "status": "Dentro do esperado"},   # sem desvio -> sem motivo
        {"talhao": "T01", "data": "2026-08-12", "status": "Abaixo do esperado"},   # abaixo, sem chuva -> só mecânica
        {"talhao": "T07", "data": "2026-08-18", "status": "Abaixo do esperado"},   # abaixo, com chuva -> mecânica + chuva
        {"talhao": "T19", "data": "2026-08-30", "status": "Acima do esperado"},    # acima, sem chuva -> só mecânica
        {"talhao": "T20", "data": "2026-08-31", "status": "Acima do esperado"},    # acima, com chuva -> mecânica + chuva
    ]

    print(f"{'Talhão':<8}{'Status':<20}{'Motivo'}")
    print("-" * 100)
    for caso in casos_de_teste:
        motivo = motivo_provavel(caso["data"], caso["status"])
        print(f"{caso['talhao']:<8}{caso['status']:<20}{motivo['texto']}")
