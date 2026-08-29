## A ideia

Comparar, por talhão, **quanto foi prescrito** de bioinsumo (definido pelo agrônomo)
com **quanto foi realmente aplicado** na lavoura — calculando o desvio entre os dois
e classificando cada aplicação como dentro ou fora do esperado.

O sistema terá dois papéis de acesso:
- **Produtor**: vê os talhões da própria fazenda
- **Colaborador Orion**: vê os talhões de todos os produtores atendidos

## Arquivos

| Arquivo | O que faz |
|---|---|
| `comparacao.py` | Calcula o desvio percentual entre dose prescrita e dose aplicada, e classifica o status (dentro / abaixo / acima do esperado) |
| `dados_exemplo.py` | 20 registros reais de aplicação (talhão, data, dose prescrita, dose aplicada), usados para testar o sistema |
| `painel.py` | Junta os dois arquivos acima: processa todos os registros de `dados_exemplo.py` usando as regras de `comparacao.py` |
| `usuarios.py` *(em desenvolvimento)* | Sistema de login com permissões diferentes para produtor e colaborador Orion |

## Como rodar

Cada arquivo pode ser testado individualmente:

```
python3 comparacao.py
python3 painel.py
```

`painel.py` imprime, para cada um dos 20 talhões, o desvio percentual e o status
calculado.

## Regra de classificação

| Desvio | Status |
|---|---|
| Até 10% (pra mais ou pra menos) | Dentro do esperado |
| Mais de 10% abaixo do prescrito | Abaixo do esperado |
| Mais de 10% acima do prescrito | Acima do esperado |

## Equipe

Letícia Correa (líder) · Laís Bueno · Giovana Lima · Amanda · Camila Dias · Camila C.

## Status do projeto

Este repositório reflete a direção atual do projeto (comparação prescrito × aplicado).
Uma ideia anterior do grupo (zoneamento de aplicação por imagem de satélite) foi
descontinuada após conversa com o professor orientador, que sugeriu um escopo mais
alinhado ao negócio principal da empresa parceira.
