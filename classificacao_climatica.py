CHUVA_DESFAVORAVEL_MM = 10
CHUVA_MODERADA_MM = 0
VENTO_DESFAVORAVEL_KMH = 15
VENTO_MODERADO_KMH = 8


def classificar_dia(chuva_mm, vento_kmh=None):

    if chuva_mm >= CHUVA_DESFAVORAVEL_MM:
        return {"classificacao": "Desfavorável", "motivo": f"Chuva de {chuva_mm}mm no dia"}

    if vento_kmh is not None and vento_kmh >= VENTO_DESFAVORAVEL_KMH:
        return {"classificacao": "Desfavorável", "motivo": f"Vento de {vento_kmh}km/h no dia"}

    if vento_kmh is not None and vento_kmh >= VENTO_MODERADO_KMH:
        return {"classificacao": "Moderado", "motivo": f"Vento moderado ({vento_kmh}km/h)"}

    if chuva_mm > CHUVA_MODERADA_MM:
        return {"classificacao": "Moderado", "motivo": f"Chuva leve ({chuva_mm}mm)"}

    return {"classificacao": "Favorável", "motivo": "Sem chuva, vento baixo"}


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
