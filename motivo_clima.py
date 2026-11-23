
from dados_clima import CLIMA_HISTORICO

# Limiares usados aqui para sinalizar clima como fator adicional no motivo do
# desvio. Propositalmente iguais aos limiares de classificacao_climatica.py,
# para que "fator adicional" citado aqui bata com a coluna de Classificação
# climática mostrada na mesma linha do dashboard.
CHUVA_RELEVANTE_MM = 10
VENTO_RELEVANTE_KMH = 15

CAUSA_MECANICA_ABAIXO = "Possível causa mecânica — verificar entupimento ou desgaste do bico"
CAUSA_MECANICA_ACIMA = "Possível causa mecânica — verificar calibração da válvula ou pressão da bomba"


def motivo_provavel(data, status):

    if status == "Dentro o esperado":
        return {"texto": "—", "tipo": "neutro"}

    if status == "Abaixo do esperado":
        texto = CAUSA_MECANICA_ABAIXO
    else:
        texto = CAUSA_MECANICA_ACIMA

    # Usa o mesmo histórico de clima real (dados_clima.py) que já alimenta
    # a classificação climática do dia, em vez de uma base fictícia à parte.
    clima_do_dia = CLIMA_HISTORICO.get(data)
    if clima_do_dia is not None:
        if clima_do_dia["chuva_mm"] >= CHUVA_RELEVANTE_MM:
            texto += f". Fator adicional: chuva de {clima_do_dia['chuva_mm']}mm registrada no dia"
        elif clima_do_dia["vento_kmh"] >= VENTO_RELEVANTE_KMH:
            texto += f". Fator adicional: vento de {clima_do_dia['vento_kmh']}km/h registrado no dia"

    return {"texto": texto, "tipo": "mecanica"}



if __name__ == "__main__":
    casos_de_teste = [
        {"talhao": "T02", "data": "2026-08-13", "status": "Dentro o esperado"},
        {"talhao": "T01", "data": "2026-08-12", "status": "Abaixo do esperado"},
        {"talhao": "T07", "data": "2026-08-18", "status": "Abaixo do esperado"},
        {"talhao": "T19", "data": "2026-08-30", "status": "Acima do esperado"},
        {"talhao": "T20", "data": "2026-08-31", "status": "Acima do esperado"},
    ]

    print(f"{'Talhão':<8}{'Status':<20}{'Motivo'}")
    print("-" * 100)
    for caso in casos_de_teste:
        motivo = motivo_provavel(caso["data"], caso["status"])
        print(f"{caso['talhao']:<8}{caso['status']:<20}{motivo['texto']}")
