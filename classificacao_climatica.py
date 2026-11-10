"""
==================================================================
CLASSIFICACAO_CLIMATICA.PY — Favorável, moderado ou desfavorável
Fábrica de Projetos | Grupo Orion x CygniAG
==================================================================

O QUE ISSO FAZ:
Recebe um dia de clima (chuva em mm, vento em km/h — opcional) e
devolve uma classificação de quão favorável aquele dia é para
aplicação de bioinsumo.

Essa MESMA função serve pras duas visões do painel:
  - "Próximos dias": aplicada sobre dados de PREVISÃO do tempo
  - "Últimos 30 dias": aplicada sobre dados HISTÓRICOS já registrados

A diferença entre as duas visões está em QUAL DADO entra na função,
não na função em si — por isso ela foi escrita separada, sem saber
se o dia que está avaliando é passado ou futuro.

REGRA:
  - chuva >= 10mm OU vento >= 15 km/h       -> Desfavorável
  - vento >= 8 km/h (mas abaixo de 15)      -> Moderado
  - chuva entre 0 e 10mm (exclusive)        -> Moderado
  - sem chuva E vento baixo (ou sem dado)   -> Favorável

Se não houver dado de vento disponível para aquele dia, a regra
usa só a chuva — o vento não entra na conta (não penaliza nem
favorece, simplesmente não é avaliado).
==================================================================
"""


CHUVA_DESFAVORAVEL_MM = 10
CHUVA_MODERADA_MM = 0
VENTO_DESFAVORAVEL_KMH = 15
VENTO_MODERADO_KMH = 8


def classificar_dia(chuva_mm, vento_kmh=None):
    """Recebe a chuva do dia (mm) e, opcionalmente, o vento (km/h).
    Devolve um dicionário com a classificação e o motivo."""

    if chuva_mm >= CHUVA_DESFAVORAVEL_MM:
        return {"classificacao": "Desfavorável", "motivo": f"Chuva de {chuva_mm}mm no dia"}

    if vento_kmh is not None and vento_kmh >= VENTO_DESFAVORAVEL_KMH:
        return {"classificacao": "Desfavorável", "motivo": f"Vento de {vento_kmh}km/h no dia"}

    if vento_kmh is not None and vento_kmh >= VENTO_MODERADO_KMH:
        return {"classificacao": "Moderado", "motivo": f"Vento moderado ({vento_kmh}km/h)"}

    if chuva_mm > CHUVA_MODERADA_MM:
        return {"classificacao": "Moderado", "motivo": f"Chuva leve ({chuva_mm}mm)"}

    return {"classificacao": "Favorável", "motivo": "Sem chuva, vento baixo"}


# ==================================================================
# TESTES
# ==================================================================

if __name__ == "__main__":
    casos_de_teste = [
        {"descricao": "Sem chuva, sem dado de vento", "chuva_mm": 0.0, "vento_kmh": None},
        {"descricao": "Chuva leve, sem dado de vento", "chuva_mm": 3.2, "vento_kmh": None},
        {"descricao": "Chuva forte", "chuva_mm": 18.7, "vento_kmh": None},
        {"descricao": "Sem chuva, vento alto", "chuva_mm": 0.0, "vento_kmh": 22},
        {"descricao": "Sem chuva, vento moderado", "chuva_mm": 0.0, "vento_kmh": 10},
        {"descricao": "Sem chuva, vento baixo", "chuva_mm": 0.0, "vento_kmh": 5},
    ]

    print(f"{'Descrição':<32}{'Chuva':<8}{'Vento':<8}{'Classificação':<16}{'Motivo'}")
    print("-" * 100)
    for caso in casos_de_teste:
        resultado = classificar_dia(caso["chuva_mm"], caso["vento_kmh"])
        vento_str = str(caso["vento_kmh"]) if caso["vento_kmh"] is not None else "—"
        print(f"{caso['descricao']:<32}{caso['chuva_mm']:<8}{vento_str:<8}{resultado['classificacao']:<16}{resultado['motivo']}")
