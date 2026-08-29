from comparacao import comparar_aplicacao
from dados_exemplo import DADOS_REAIS

for registro in DADOS_REAIS:
    resultado = comparar_aplicacao(registro["dose_prescrita"], registro["dose_aplicada"])
    print(registro["talhao"], resultado)