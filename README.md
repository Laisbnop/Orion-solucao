# Orion-solucao

Projeto da disciplina **Fábrica de Projetos** (Bacharelado em Ciência da Computação),
em parceria com a empresa **Orion** — fabricante de equipamentos para aplicação de
bioinsumos no sulco de plantio.

## A ideia

Comparar, por talhão, **quanto foi prescrito** de bioinsumo (definido pelo agrônomo)
com **quanto foi realmente aplicado** na lavoura — calculando o desvio entre os dois,
classificando cada aplicação como dentro ou fora do esperado, e sugerindo um **motivo
provável** para o desvio, cruzando com dados de clima do dia da aplicação.

O sistema tem dois papéis de acesso:
- **Produtor**: vê os talhões da própria fazenda
- **Colaborador Orion**: vê os talhões de todos os produtores atendidos

## Arquivos

| Arquivo | O que faz | Responsável |
|---|---|---|
| `dados_exemplo.py` | 20 registros reais de aplicação (talhão, data, dose prescrita, dose aplicada) | Letícia |
| `comparacao.py` | Calcula o desvio percentual entre dose prescrita e dose aplicada, e classifica o status (dentro / abaixo / acima do esperado) | Laís |
| `usuarios.py` | Login com múltiplos produtores e colaboradores Orion, cadastro (nome, email, fazenda) e filtro por permissão | Camila Dias |
| `motivo_clima.py` | Sugere um motivo provável para desvios fora do esperado, cruzando a data da aplicação com dados de clima | Laís |
| `painel.py` | Junta as peças acima: login → filtro por permissão → cálculo de desvio → motivo provável | Laís + Camila Dias |

## Como rodar

Cada arquivo pode ser testado individualmente:

```
python3 comparacao.py
python3 usuarios.py
python3 motivo_clima.py
python3 painel.py
```

`painel.py` mostra, para o usuário logado no teste, uma saudação personalizada e a
lista de talhões visíveis com desvio, status e motivo provável.

## Usuários de teste

| Usuário | Senha | Papel | Vê |
|---|---|---|---|
| `produtor1` | `santaluzia123` | Produtor | Fazenda Santa Luzia (5 talhões) |
| `produtor2` | `boavista123` | Produtor | Fazenda Boa Vista (5 talhões) |
| `produtor3` | `rioverde123` | Produtor | Fazenda Rio Verde (10 talhões) |
| `agronomo1` | `orion123` | Colaborador Orion | Todos os 20 talhões |
| `agronomo2` | `orion456` | Colaborador Orion | Todos os 20 talhões |

## Regra de classificação do desvio

| Desvio | Status |
|---|---|
| Até 10% (pra mais ou pra menos) | Dentro do esperado |
| Mais de 10% abaixo do prescrito | Abaixo do esperado |
| Mais de 10% acima do prescrito | Acima do esperado |

## Regra do motivo provável

Quando um talhão fica **fora do esperado**, o sistema verifica se choveu no dia da
aplicação (chuva ≥ 10mm) e, se sim, sugere isso como possível causa do desvio.

| Situação | Motivo mostrado |
|---|---|
| Desvio dentro do esperado | — (não se aplica) |
| Fora do esperado, choveu ≥ 10mm no dia | "Possível chuva no dia (X mm)" |
| Fora do esperado, sem chuva relevante | "Sem causa climática aparente" |
| Fora do esperado, sem dado de clima daquela data | "Sem dado climático disponível" |

### ⚠️ Sobre a origem dos dados de clima

Os dados de **aplicação** (talhão, data, dose prescrita, dose aplicada) são **reais**,
fornecidos pela empresa parceira.

Os dados de **clima** usados em `motivo_clima.py` são **fictícios**. O grupo recebeu um
arquivo real de previsão do tempo da fazenda, mas o período coberto pelas datas de
aplicação disponíveis não registrou chuva significativa — o que impediria demonstrar a
funcionalidade de correlação clima-desvio com dado 100% real. Para contornar isso, foi
criado um conjunto de dados climáticos fictício, mantendo a mesma estrutura (chuva em
mm, temperatura em °C) do dado real fornecido pela empresa, com valores variados de
propósito para cobrir os dois cenários (com e sem chuva).

Essa decisão foi validada com o professor orientador, que autorizou o uso de dados
fictícios desde que a funcionalidade fizesse sentido e funcionasse de fato.

## Equipe

| Integrante | Frente |
|---|---|
| Letícia Correa | Líder · dados de exemplo · contato com a empresa parceira |
| Laís Bueno | Regra de comparação · motivo do desvio (clima) · integração no painel |
| Camila Dias | Sistema de login e permissões |
| Giovana Lima | Interface visual do dashboard |
| Amanda | Apoio no dashboard |
| Camila C. | Testes de ponta a ponta · apresentação |

## Status do projeto

- ✅ Cálculo de desvio e status
- ✅ Login com múltiplos papéis e permissões
- ✅ Motivo provável do desvio (clima)
- ✅ Painel unificado, testado via terminal
- 🔲 Servidor web (Flask) — em andamento
- 🔲 Interface visual no navegador — planejado
- 🔲 Gráficos e comparações — planejado

Este repositório reflete a direção atual do projeto (comparação prescrito × aplicado,
com motivo provável). Uma ideia anterior do grupo (zoneamento de aplicação por imagem
de satélite) foi descontinuada após conversa com o professor orientador, que sugeriu
um escopo mais alinhado ao negócio principal da empresa parceira. Uma segunda ideia
(sensor físico de vazão) também foi ajustada, por envolver complexidade mecânica além
do escopo da disciplina.
