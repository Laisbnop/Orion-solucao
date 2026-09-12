USUARIOS = {
    "produtor1": {
        "senha": "santaluzia123",
        "papel": "produtor",
        "nome": "Rafael Castanha",
        "email": "rafael.castanha@santaluzia.com.br",
        "fazenda": "Fazenda Santa Luzia",
        "talhoes_visiveis": ["T01", "T02", "T03", "T04", "T05"],
    },
    "produtor2": {
        "senha": "boavista123",
        "papel": "produtor",
        "nome": "Letícia Correa",
        "email": "leticia.correa@boavista.com.br",
        "fazenda": "Fazenda Boa Vista",
        "talhoes_visiveis": ["T06", "T07", "T08", "T09", "T10"],
    },
    "produtor3": {
        "senha": "rioverde123",
        "papel": "produtor",
        "nome": "Renan Ferraroni",
        "email": "renan.ferraroni@rioverde.com.br",
        "fazenda": "Fazenda Rio Verde",
        "talhoes_visiveis": ["T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19", "T20"],
    },    

    #COLABORADORES ORION
        "agronomo1": {
        "senha": "orion123",
        "papel": "orion",
        "nome": "Camila Dias",
        "email": "camila.dias@orion.ind.br",
        "fazenda": None,  # colaborador Orion não tem fazenda própria
        "talhoes_visiveis": ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09", "T10",
                              "T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19", "T20"],
    },
    "agronomo2": {
        "senha": "orion456",
        "papel": "orion",
        "nome": "Lais Bueno",
        "email": "lais.bueno@orion.ind.br",
        "fazenda": None,
        "talhoes_visiveis": ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09", "T10",
                              "T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19", "T20"],
    }
}

def fazer_login(usuario, senha):
    if usuario not in USUARIOS:
        return {"sucesso": False, "motivo": "Usuário não encontrado"}
    dados_usuario = USUARIOS[usuario]
 
    if dados_usuario["senha"] != senha:
        return {"sucesso": False, "motivo": "Senha incorreta"}
    return {
        "sucesso": True,
        "papel": dados_usuario["papel"],
        "nome": dados_usuario["nome"],
        "email": dados_usuario["email"],
        "fazenda": dados_usuario["fazenda"],
    }
 
def filtrar_dados_por_permissao(lista_de_aplicacoes, talhoes_visiveis):
    resultado = []
    for aplicacao in lista_de_aplicacoes:
        if aplicacao["talhao"] in talhoes_visiveis:
            resultado.append(aplicacao)
    return resultado


 # TESTES
if __name__ == "__main__":
    print("=== Login de cada produtor ===")
    for usuario in ["produtor1", "produtor2", "produtor3"]:
        senha = USUARIOS[usuario]["senha"]
        resultado = fazer_login(usuario, senha)
        print(f"{usuario}: {resultado['nome']} ({resultado['fazenda']}) — {resultado['email']}")
 
    print()
    print("=== Login de cada agrônomo ===")
    for usuario in ["agronomo1", "agronomo2"]:
        senha = USUARIOS[usuario]["senha"]
        resultado = fazer_login(usuario, senha)
        talhoes = USUARIOS[usuario]["talhoes_visiveis"]
        print(f"{usuario}: {resultado['nome']} — vê {len(talhoes)} talhões (todos)")
 
    print()
    print("=== Erros continuam funcionando? ===")
    print(fazer_login("produtor1", "senhaerrada"))
    print(fazer_login("naoexiste", "qualquer"))