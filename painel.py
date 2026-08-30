from comparacao import comparar_aplicacao
from dados_exemplo import DADOS_REAIS
from usuarios import fazer_login, filtrar_dados_por_permissao, USUARIOS

def montar_painel(usuario, senha):
    login = fazer_login(usuario, senha)

    if not login["sucesso"]:
        return {"sucesso": False, "motivo": login["motivo"]}

    talhoes_visiveis = USUARIOS[usuario]["talhoes_visiveis"]
    dados_visiveis = filtrar_dados_por_permissao(DADOS_REAIS, talhoes_visiveis)

    aplicacoes_com_resultado = []
    for registro in dados_visiveis:
        resultado = comparar_aplicacao(registro["dose_prescrita"], registro["dose_aplicada"])
        aplicacoes_com_resultado.append({**registro, **resultado})

    return {"sucesso": True, "papel": login["papel"], "aplicacoes": aplicacoes_com_resultado}


painel_produtor = montar_painel("produtor1", "santaluzia123")
for aplicacao in painel_produtor["aplicacoes"]:
    print(aplicacao["talhao"], aplicacao["desvio_pct"], aplicacao["status"])