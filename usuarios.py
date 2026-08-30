USUARIOS = {
    "produtor1": {
        "senha": "santaluzia123",
        "papel": "produtor",
        "talhoes_visiveis": ["T01", "T02", "T03", "T04", "T05"],
    },
    "agronomo1": {
        "senha": "orion123",
        "papel": "orion",
        "talhoes_visiveis": ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09", "T10",
                              "T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19", "T20"],
    },
}

def fazer_login (usuario, senha):
    if usuario not in USUARIOS:
        return {"sucesso": False, "motivo": "Usuário não encontrado"}
    
    dados_usuario = USUARIOS[usuario]

    if dados_usuario ["senha"] != senha:
        return {"sucesso": False, "motivo": "Senha incorreta"}

    return {"sucesso": True, "papel": dados_usuario["papel"]}

def filtrar_dados_por_permissao(lista_de_aplicacoes, talhoes_visiveis):
    resultado = []
    for aplicacao in lista_de_aplicacoes:
        if aplicacao ["talhao"] in talhoes_visiveis:
            resultado.append(aplicacao)
    return resultado

print(fazer_login("produtor1", "santaluzia123"))
print(fazer_login("produtor1", "senhaerrada"))
print(fazer_login("naoexiste", "qualquer"))

from dados_exemplo import DADOS_REAIS

login = fazer_login ("produtor1", "santaluzia123")
talhoes_do_produtor = USUARIOS["produtor1"]["talhoes_visiveis"]
dados_filtrados = filtrar_dados_por_permissao(DADOS_REAIS, talhoes_do_produtor)

print(f"O produtor1 pode ver {len(dados_filtrados)} de {len(DADOS_REAIS)} registros")