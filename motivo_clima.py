# CONFIGURAÇÃO
CHUVA_RELEVANTE_MM = 10  # a partir de quantos mm a chuva "conta" como motivo
# DADO FICTÍCIO — clima por data (mm de chuva, temperatura média)
# Mesma estrutura do arquivo real fornecido pela empresa parceira
# (chuva em mm, temperatura em °C), só que com valores inventados
# para cobrir as 20 datas de aplicação
 
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
def motivo_provavel(data, status):
    """Função principal: recebe a data da aplicação (texto, formato
    "AAAA-MM-DD") e o status do desvio (texto vindo do comparacao.py
    de vocês: "Dentro do esperado", "Abaixo do esperado" ou "Acima
    do esperado"), e devolve um dicionário com o motivo provável.
 
    Exemplo de uso:
        from comparacao import comparar_aplicacao
        from motivo_clima import motivo_provavel
 
        resultado = comparar_aplicacao(200, 178)
        motivo = motivo_provavel("2026-08-29", resultado["status"])
    """

    if status == "Dentro do esperado":
        return {"texto": "—", "tipo": "neutro"}
    clima_do_dia = CLIMA_FICTICIO.get(data)
    if clima_do_dia is None:
        return {"texto": "Sem dado climático disponível", "tipo": "sem_dado"}
    if clima_do_dia["chuva_mm"] >= CHUVA_RELEVANTE_MM:
        return {
            "texto": f"Possível chuva no dia ({clima_do_dia['chuva_mm']}mm)",
            "tipo": "chuva",
        }
    return {"texto": "Sem causa climática aparente", "tipo": "sem_causa"}
 
# TESTES 
if __name__ == "__main__":
    casos_de_teste = [
        {"talhao": "T02", "data": "2026-08-13", "status": "Dentro do esperado"},  # sem motivo
        {"talhao": "T07", "data": "2026-08-18", "status": "Abaixo do esperado"},  # choveu -> motivo: chuva
        {"talhao": "T01", "data": "2026-08-12", "status": "Abaixo do esperado"},  # sem chuva -> sem causa
        {"talhao": "T99", "data": "2026-09-15", "status": "Acima do esperado"},   # data sem clima -> sem dado
    ]
 
    print(f"{'Talhão':<8}{'Data':<14}{'Status':<20}{'Motivo'}")
    print("-" * 75)
    for caso in casos_de_teste:
        motivo = motivo_provavel(caso["data"], caso["status"])
        print(f"{caso['talhao']:<8}{caso['data']:<14}{caso['status']:<20}{motivo['texto']}")
 