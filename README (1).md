# Orion-solucao

Projeto da disciplina **Fábrica de Projetos** (Bacharelado em Ciência da Computação),
em parceria com a empresa **Orion** — fabricante de equipamentos para aplicação de
bioinsumos no sulco de plantio.

## A ideia

Um painel que calcula, a partir de dados reais de clima (chuva e vento), o quanto cada
dia favorece ou atrapalha a aplicação de bioinsumo na lavoura — ajudando o produtor e a
equipe da Orion a entender o contexto de cada aplicação.

O sistema classifica cada dia em três categorias — **Favorável**, **Moderado** ou
**Desfavorável** — com base em regras objetivas sobre chuva e vento, aplicadas sobre
histórico real de clima fornecido pela própria empresa parceira.

O sistema tem dois papéis de acesso:
- **Produtor**: vê os talhões da própria fazenda
- **Colaborador Orion**: vê os talhões de todos os produtores atendidos

## Arquivos

| Arquivo | O que faz |
|---|---|
| `classificacao_climatica.py` | Função principal: recebe chuva (mm) e vento (km/h) de um dia e devolve Favorável / Moderado / Desfavorável |
| `dados_clima.py` | Histórico real de clima — 159 dias, com chuva e vento, fornecido pela empresa parceira |
| `dados_exemplo.py` | 20 registros reais de talhão, produtor e data, usados para ligar cada talhão à data de clima correspondente |
| `usuarios.py` | Login, cadastro de usuários e filtro de dados por permissão |
| `painel.py` | Orquestração: junta login, permissões e classificação climática em um resultado único por talhão |
| `app.py` | Servidor Flask — expõe `painel.py` como API HTTP (rota `/login`) |
| `comparacao.py`, `motivo_clima.py` | Lógica do projeto anterior (comparação entre dose prescrita e dose aplicada), mantidos como registro da evolução do projeto — ver seção "Histórico do projeto" |
| `index.html`, `css.zip`, `js.zip`, `orion-frontend.zip` | Protótipo de interface visual iniciado para o projeto anterior; não finalizado — o grupo optou por concentrar o tempo disponível na robustez da lógica de back-end |

## Como rodar

```
pip install flask
python3 app.py
```

O servidor fica disponível em `http://127.0.0.1:5000`. A rota principal:

```
GET/POST /login
Parâmetros: usuario, senha
```

Cada módulo também pode ser testado individualmente:

```
python3 classificacao_climatica.py
python3 usuarios.py
python3 painel.py
```

`painel.py` imprime, para o usuário de teste logado, a classificação climática de cada
talhão visível a ele.

## Usuários de teste

| Usuário | Senha | Papel | Vê |
|---|---|---|---|
| `produtor1` | `santaluzia123` | Produtor | Fazenda Santa Luzia (5 talhões) |
| `produtor2` | `boavista123` | Produtor | Fazenda Boa Vista (5 talhões) |
| `produtor3` | `rioverde123` | Produtor | Fazenda Rio Verde (10 talhões) |
| `agronomo1` | `orion123` | Colaborador Orion | Todos os 20 talhões |
| `agronomo2` | `orion456` | Colaborador Orion | Todos os 20 talhões |

## Regra de classificação

| Condição | Classificação |
|---|---|
| Chuva ≥ 10mm, ou vento ≥ 15 km/h | Desfavorável |
| Vento entre 8 e 15 km/h, ou chuva leve (0–10mm) | Moderado |
| Sem chuva e vento baixo | Favorável |

Aplicada sobre os 159 dias reais de clima da fazenda, essa regra resulta em uma
distribuição equilibrada: 44% dos dias favoráveis, 49% moderados e 7% desfavoráveis.

### Sobre a origem dos dados

Os dados de **clima** (`dados_clima.py`) são **reais**, fornecidos pela empresa
parceira via captura meteorológica. Os dados de **talhão/data** (`dados_exemplo.py`)
também são reais. Como o período de clima disponível cobre de 19/03 a 26/08/2026, 5 dos
20 talhões têm datas fora desse intervalo — nesses casos, o sistema retorna "Sem dado
disponível" de forma explícita, em vez de inventar um valor.

## Histórico do projeto

Este é o terceiro direcionamento do projeto:

1. **Zoneamento de aplicação por imagem de satélite** (índices NDVI/ARVI) — descontinuado
   após orientação do professor, que sugeriu um escopo mais alinhado ao negócio principal
   da empresa parceira.
2. **Comparação entre dose prescrita e dose aplicada pela máquina** — descontinuado após
   o professor apontar que a Orion não possui, hoje, tecnologia para medir a dose
   aplicada com precisão, tornando o dado central do cálculo inviável.
3. **Classificação climática para apoio à decisão de aplicação** (direção atual) — usa
   dado que realmente existe e é mensurável (clima), resolvendo o problema de
   viabilidade apontado na direção anterior.

A lógica de permissões e login construída nas versões anteriores foi mantida e
reaproveitada integralmente na versão atual.

Nesta etapa, o grupo decidiu concentrar o tempo disponível na robustez da lógica de
back-end — testada e documentada — em vez de finalizar uma interface visual elaborada.
Um protótipo de interface iniciado para a versão anterior do projeto permanece no
repositório (`index.html`, `css.zip`, `js.zip`, `orion-frontend.zip`), mas não foi
atualizado para a lógica atual.

## Equipe

Letícia Correa (líder) · Laís Bueno · Giovana Lima · Amanda · Camila Dias · Camila C.
