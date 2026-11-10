"""
==================================================================
PAINEL.PY — Orquestração (versão clima)
Fábrica de Projetos | Grupo Orion x CygniAG
==================================================================

Junta login, permissões e classificação climática em um resultado
único. Para cada talhão visível ao usuário logado, busca o clima
real da data daquele registro e classifica o dia em Favorável,
Moderado ou Desfavorável.

Nem toda data em dados_exemplo.py tem clima correspondente em
dados_clima.py — quando não houver, o talhão aparece com
classificação "Sem dado disponível", em vez de quebrar ou inventar
um valor.
==================================================================
"""

from dados_exemplo import DADOS_REAIS
from dados_clima import CLIMA_HISTORICO
from usuarios import fazer_login, filtrar_dados_por_permissao, USUARIOS
from classificacao_climatica import classificar_dia


def montar_painel(usuario, senha):
    login = fazer_login(usuario, senha)

    if not login["sucesso"]:
        return {"sucesso": False, "motivo": login["motivo"]}

    talhoes_visiveis = USUARIOS[usuario]["talhoes_visiveis"]
    dados_visiveis = filtrar_dados_por_permissao(DADOS_REAIS, talhoes_visiveis)

    talhoes_com_resultado = []
    for registro in dados_visiveis:
        clima_do_dia = CLIMA_HISTORICO.get(registro["data"])

        if clima_do_dia is None:
            resultado = {"classificacao": "Sem dado disponível", "motivo": "Data fora do período com clima registrado"}
        else:
            resultado = classificar_dia(clima_do_dia["chuva_mm"], clima_do_dia["vento_kmh"])

        talhoes_com_resultado.append({
            "talhao": registro["talhao"],
            "produtor": registro["produtor"],
            "data": registro["data"],
            "chuva_mm": clima_do_dia["chuva_mm"] if clima_do_dia else None,
            "vento_kmh": clima_do_dia["vento_kmh"] if clima_do_dia else None,
            "classificacao": resultado["classificacao"],
            "motivo": resultado["motivo"],
        })

    return {
        "sucesso": True,
        "papel": login["papel"],
        "nome": login["nome"],
        "fazenda": login["fazenda"],
        "talhoes": talhoes_com_resultado,
    }


# ==================================================================
# TESTES
# ==================================================================

if __name__ == "__main__":
    painel_produtor = montar_painel("produtor1", "santaluzia123")
    if painel_produtor["fazenda"]:
        print(f"Bem-vindo, {painel_produtor['nome']} — {painel_produtor['fazenda']}")
    else:
        print(f"Bem-vindo, {painel_produtor['nome']} (Equipe Orion)")
    for talhao in painel_produtor["talhoes"]:
        print(talhao["talhao"], talhao["data"], "-", talhao["classificacao"], f"({talhao['motivo']})")

    print()
    print("=== Testando produtor3 (inclui talhões sem clima disponível) ===")
    painel_produtor3 = montar_painel("produtor3", "rioverde123")
    for talhao in painel_produtor3["talhoes"]:
        print(talhao["talhao"], talhao["data"], "-", talhao["classificacao"], f"({talhao['motivo']})")

    print()
    print("=== Testando agronomo1 (vê todos os 20 talhões) ===")
    painel_orion = montar_painel("agronomo1", "orion123")
    print(f"Total de talhões visíveis: {len(painel_orion['talhoes'])}")

    print()
    print("=== Erro de login continua funcionando? ===")
    print(montar_painel("produtor1", "senhaerrada"))
