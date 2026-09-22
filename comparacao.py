def calcular_desvio(dose_prescrita, dose_aplicada):
    desvio = (dose_aplicada - dose_prescrita) / dose_prescrita * 100
    return round (desvio, 1)

def classificar_status(desvio_pct):
    if abs (desvio_pct) <= 10:
        return "Dentro o esperado"
    elif desvio_pct < 0:
        return "Abaixo do esperado"
    else:
        return "Acima do esperado"

def comparar_aplicacao(dose_prescrita, dose_aplicada):
    desvio = calcular_desvio(dose_prescrita, dose_aplicada)
    status = classificar_status(desvio)
    return {"desvio_pct": desvio, "status": status}