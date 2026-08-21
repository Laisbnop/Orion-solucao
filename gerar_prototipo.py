"""
==================================================================
GERADOR DO PROTÓTIPO HTML — a partir dos dados reais processados
Fábrica de Projetos | Grupo Orion x CygniAG
==================================================================

O QUE ISSO FAZ:
Roda o mesmo processamento do process_indice.py, mas em vez de só
salvar .json/.png separados, MONTA O ARQUIVO HTML INTEIRO com todos
os índices encontrados, prontos pra abrir no navegador e comparar.

Ou seja: isso substitui o prototipo_zoneamento_arvi.html antigo (que
só tinha ARVI) por uma versão que se adapta sozinha a quantos
índices existirem na pasta — 1, 11, ou 30.

COMO USAR:
1. Ajuste PASTA_ENTRADA lá embaixo pra apontar pra pasta com as
   imagens (a mesma que vocês já usam no process_indice.py)
2. Rode: python3 gerar_prototipo.py
3. Abre o arquivo prototipo.html que aparecer do lado do script
==================================================================
"""

import json
import re
import base64
from pathlib import Path
from PIL import Image


# ==================================================================
# CONFIGURAÇÃO — mexam aqui
# ==================================================================
PASTA_ENTRADA = "/Users/lais/Desktop/projeto-orion-cygnia/sentinel-21-07"                # pasta com os PNGs de índice
ARQUIVO_SAIDA = "prototipo.html"   # nome do HTML gerado
ESCALA_PADRAO = "0_100"            # escala preferida por índice
CELL_SIZE = 15
TAMANHO_MINIMO_VALIDO = 1000       # bytes — pula arquivos "cloudy" vazios


# ==================================================================
# MESMA LÓGICA DE SEMPRE (Laís + Letícia) — sem mudanças
# ==================================================================

def carregar_imagem(caminho):
    img = Image.open(caminho).convert("RGBA")
    return img, img.size


def calcular_score_pixel(r, g, b, a, g_min, g_max):
    if a == 0:
        return None
    if g_max == g_min:
        return 50.0
    return (g - g_min) / (g_max - g_min) * 100


def processar_imagem(caminho, cell_size=CELL_SIZE):
    img, (largura, altura) = carregar_imagem(caminho)
    px = img.load()

    valores_verde = [
        px[x, y][1]
        for x in range(largura)
        for y in range(altura)
        if px[x, y][3] > 0
    ]
    if not valores_verde:
        return [], img

    g_min, g_max = min(valores_verde), max(valores_verde)
    zonas = []
    zone_id = 1
    linhas = (altura + cell_size - 1) // cell_size
    colunas = (largura + cell_size - 1) // cell_size

    for row in range(linhas):
        for col in range(colunas):
            x0, y0 = col * cell_size, row * cell_size
            x1, y1 = min(x0 + cell_size, largura), min(y0 + cell_size, altura)
            scores_da_zona = []
            for x in range(x0, x1):
                for y in range(y0, y1):
                    r, g, b, a = px[x, y]
                    score = calcular_score_pixel(r, g, b, a, g_min, g_max)
                    if score is not None:
                        scores_da_zona.append(score)
            if not scores_da_zona:
                continue
            media = sum(scores_da_zona) / len(scores_da_zona)
            zonas.append({"id": zone_id, "row": row, "col": col, "avg_score": round(media, 1)})
            zone_id += 1

    return zonas, img


def classificar_zona(avg_score):
    if avg_score < 33:
        return "Baixa"
    elif avg_score < 66:
        return "Média"
    else:
        return "Alta"


def dose_recomendada(categoria):
    return {"Baixa": 115, "Média": 100, "Alta": 85}[categoria]


def aplicar_classificacao(zonas):
    for zona in zonas:
        categoria = classificar_zona(zona["avg_score"])
        zona["category"] = categoria
        zona["dose_pct"] = dose_recomendada(categoria)
    return zonas


def gerar_mapa_de_zonas(img, zonas, cell_size=CELL_SIZE):
    cores = {"Baixa": (214, 69, 65), "Média": (232, 168, 56), "Alta": (58, 143, 92)}
    largura, altura = img.size
    px = img.load()
    overlay = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    overlay_px = overlay.load()
    for zona in zonas:
        x0, y0 = zona["col"] * cell_size, zona["row"] * cell_size
        x1 = min(x0 + cell_size, largura)
        y1 = min(y0 + cell_size, altura)
        cor = cores[zona["category"]]
        for x in range(x0, x1):
            for y in range(y0, y1):
                if px[x, y][3] > 0:
                    overlay_px[x, y] = (*cor, 235)
    return overlay


PADRAO_ARQUIVO = re.compile(r"^([a-z0-9]+)_cloudless_(.+)\.png$")


def descobrir_indices(pasta):
    pasta = Path(pasta)
    indices = {}
    for arquivo in pasta.glob("*_cloudless_*.png"):
        m = PADRAO_ARQUIVO.match(arquivo.name)
        if not m:
            continue
        indice, escala = m.group(1), m.group(2)
        if arquivo.stat().st_size < TAMANHO_MINIMO_VALIDO:
            continue
        indices.setdefault(indice, []).append(escala)
    return indices


def imagem_para_base64(img):
    """Converte uma imagem PIL (já carregada) em base64, sem salvar em disco."""
    import io
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


# ==================================================================
# NOVIDADE: monta os dados de TODOS os índices pro HTML
# ==================================================================

def montar_datasets(pasta_entrada=PASTA_ENTRADA, escala=ESCALA_PADRAO):
    pasta_entrada = Path(pasta_entrada)
    indices_encontrados = descobrir_indices(pasta_entrada)

    if not indices_encontrados:
        print("Nenhum índice encontrado. Confira o PASTA_ENTRADA.")
        return {}

    datasets = {}
    for indice, escalas_disponiveis in sorted(indices_encontrados.items()):
        escala_usar = escala if escala in escalas_disponiveis else escalas_disponiveis[0]
        caminho = pasta_entrada / f"{indice}_cloudless_{escala_usar}.png"

        zonas, img_original = processar_imagem(caminho)
        if not zonas:
            print(f"  [{indice}] pulado — sem dado válido")
            continue

        zonas = aplicar_classificacao(zonas)
        mapa_zonas = gerar_mapa_de_zonas(img_original, zonas)

        datasets[indice] = {
            "label": f"{indice.upper()} · escala {escala_usar}",
            "orig": imagem_para_base64(img_original),
            "zonemap": imagem_para_base64(mapa_zonas),
            "zonas": zonas,
        }
        print(f"  [{indice}] escala usada: {escala_usar} -> {len(zonas)} zonas")

    return datasets


# ==================================================================
# TEMPLATE DO HTML
# ==================================================================

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Zoneamento de Aplicação — Protótipo</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');

:root{
  --soil-950:#12160f; --soil-900:#181d14; --soil-800:#232a1c; --soil-700:#333b28;
  --paper:#f3efe4; --paper-dim:#c9c2ad;
  --green:#4a9163; --green-dim:#3a8f5c33;
  --amber:#e0a83e; --amber-dim:#e0a83e33;
  --red:#cf5147; --red-dim:#cf514733;
  --line: rgba(243,239,228,0.12);
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{
  background: radial-gradient(ellipse 900px 500px at 15% -10%, #24301f 0%, transparent 60%), var(--soil-950);
  color:var(--paper); font-family:'Inter',sans-serif; min-height:100vh; padding:0 0 80px;
}
::selection{ background:var(--green); color:var(--soil-950); }
.wrap{ max-width:1080px; margin:0 auto; padding:0 28px; }
header{ padding:56px 0 40px; border-bottom:1px solid var(--line); }
.eyebrow{
  font-family:'IBM Plex Mono', monospace; font-size:12.5px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--green); display:flex; align-items:center; gap:10px; margin-bottom:22px;
}
.eyebrow::before{ content:''; width:7px; height:7px; background:var(--green); border-radius:50%; box-shadow:0 0 0 4px var(--green-dim); }
h1{ font-family:'Fraunces', serif; font-weight:500; font-size:clamp(32px, 5vw, 52px); line-height:1.05; margin:0 0 18px; letter-spacing:-0.01em; }
h1 em{ font-style:italic; font-weight:300; color:var(--paper-dim); }
.dek{ font-size:16.5px; line-height:1.65; color:var(--paper-dim); max-width:620px; margin:0; }
.meta-row{ display:flex; flex-wrap:wrap; gap:10px; margin-top:28px; }
.tag{ font-family:'IBM Plex Mono', monospace; font-size:11.5px; padding:6px 12px; border:1px solid var(--line); border-radius:100px; color:var(--paper-dim); }
.notice{ margin-top:32px; padding:18px 20px; background:var(--soil-800); border-left:2px solid var(--amber); border-radius:2px; font-size:13.5px; line-height:1.6; color:var(--paper-dim); }
.notice b{ color:var(--paper); font-weight:600; }
.section{ padding:56px 0; border-bottom:1px solid var(--line); }
.section:last-of-type{ border-bottom:none; }
.section-num{ font-family:'IBM Plex Mono', monospace; font-size:12px; color:var(--green); letter-spacing:.1em; }
.section h2{ font-family:'Fraunces', serif; font-weight:500; font-size:26px; margin:8px 0 12px; }
.section > p.lead{ color:var(--paper-dim); font-size:14.5px; line-height:1.6; max-width:600px; margin:0 0 32px; }

.index-picker{ margin-bottom:32px; }
.index-picker label{
  display:block; font-family:'IBM Plex Mono', monospace; font-size:11px; text-transform:uppercase;
  letter-spacing:.08em; color:var(--paper-dim); margin-bottom:10px;
}
.index-picker select{
  font-family:'IBM Plex Mono', monospace; font-size:14px; background:var(--soil-800); color:var(--paper);
  border:1px solid var(--line); border-radius:6px; padding:10px 14px; min-width:260px; cursor:pointer;
}
.index-picker select:focus{ outline:1px solid var(--green); }

.compare{ display:grid; grid-template-columns:1fr 1fr; gap:1px; background:var(--line); border:1px solid var(--line); border-radius:4px; overflow:hidden; }
.compare-panel{ background:var(--soil-900); padding:26px; }
.compare-panel-label{ font-family:'IBM Plex Mono', monospace; font-size:11px; text-transform:uppercase; letter-spacing:.08em; color:var(--paper-dim); margin-bottom:16px; display:flex; justify-content:space-between; }
.img-frame{ background: repeating-conic-gradient(#1d231a 0% 25%, #202619 0% 50%) 50% / 16px 16px; border-radius:3px; display:flex; align-items:center; justify-content:center; padding:20px; }
.img-frame img{ width:100%; max-width:340px; image-rendering:pixelated; display:block; }

.legend{ display:flex; gap:22px; margin-top:20px; flex-wrap:wrap; }
.legend-item{ display:flex; align-items:center; gap:8px; font-family:'IBM Plex Mono', monospace; font-size:12px; color:var(--paper-dim); }
.dot{ width:10px; height:10px; border-radius:2px; flex-shrink:0; }

.kpi-strip{ display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--line); border:1px solid var(--line); border-radius:4px; overflow:hidden; margin-bottom:40px; }
.kpi{ background:var(--soil-900); padding:22px 20px; }
.kpi-label{ font-family:'IBM Plex Mono', monospace; font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:var(--paper-dim); margin-bottom:10px; }
.kpi-value{ font-family:'Fraunces', serif; font-size:30px; font-weight:500; }
.kpi-value.low{ color:var(--red); } .kpi-value.mid{ color:var(--amber); } .kpi-value.high{ color:var(--green); }

.table-wrap{ border:1px solid var(--line); border-radius:4px; overflow:hidden; }
.table-scroll{ max-height:420px; overflow-y:auto; }
table{ width:100%; border-collapse:collapse; font-size:13.5px; }
thead th{ position:sticky; top:0; background:var(--soil-800); text-align:left; font-family:'IBM Plex Mono', monospace; font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:var(--paper-dim); padding:12px 16px; border-bottom:1px solid var(--line); }
tbody td{ padding:11px 16px; border-bottom:1px solid var(--line); color:var(--paper); }
tbody tr:last-child td{ border-bottom:none; }
tbody tr:hover{ background:var(--soil-800); }
.badge{ display:inline-flex; align-items:center; gap:6px; padding:3px 10px 3px 8px; border-radius:100px; font-family:'IBM Plex Mono', monospace; font-size:11.5px; }
.badge::before{ content:''; width:6px; height:6px; border-radius:50%; }
.badge.low{ background:var(--red-dim); color:#f0a49c; } .badge.low::before{ background:var(--red); }
.badge.mid{ background:var(--amber-dim); color:#f5cb8a; } .badge.mid::before{ background:var(--amber); }
.badge.high{ background:var(--green-dim); color:#93cfa8; } .badge.high::before{ background:var(--green); }
.mono{ font-family:'IBM Plex Mono', monospace; color:var(--paper-dim); }

footer{ padding-top:48px; text-align:center; }
footer p{ font-family:'IBM Plex Mono', monospace; font-size:11.5px; color:var(--paper-dim); letter-spacing:.02em; }

@media (max-width:720px){ .compare{ grid-template-columns:1fr; } .kpi-strip{ grid-template-columns:1fr 1fr; } }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="eyebrow">Fábrica de Projetos &middot; Grupo Orion &times; CygniAG</div>
    <h1>Zoneamento de aplicação<br><em>a partir dos índices de vegetação</em></h1>
    <p class="dek">Protótipo que transforma os mapas exportados pela CygniAG em zonas de talhão
      classificadas — servindo de base para uma recomendação de dose diferenciada de bioinsumo,
      pensando na aplicação da Orion.</p>
    <div class="meta-row">
      <span class="tag">__QTD_INDICES__ índices disponíveis</span>
      <span class="tag">Python (Pillow) + HTML/CSS/JS</span>
      <a href="mapa.html" style="font-family:'IBM Plex Mono', monospace; font-size:11.5px; padding:6px 12px; border:1px solid var(--green); border-radius:100px; color:var(--green); text-decoration:none;">Ver no mapa real →</a>
    </div>
    <div class="notice">
      <b>Isso é um protótipo.</b> A conversão de cor → valor de índice é uma
      <b>aproximação simplificada</b> (baseada no canal verde da imagem), não o dado bruto real da
      CygniAG. Índices diferentes medem coisas diferentes (vigor, clorofila, umidade...), então
      compare com atenção — a heurística pode não ser igualmente justa entre eles.
    </div>
  </header>

  <section class="section">
    <div class="section-num">01 — ÍNDICE</div>
    <h2>Escolha o índice para visualizar</h2>
    <p class="lead">Cada índice foi processado separadamente. Selecione um para ver o
      zoneamento gerado a partir dele.</p>

    <div class="index-picker">
      <label>Índice de vegetação</label>
      <select id="index-select"></select>
    </div>

    <div class="compare">
      <div class="compare-panel">
        <div class="compare-panel-label"><span>Original</span><span id="label-orig"></span></div>
        <div class="img-frame"><img id="img-orig" alt="Mapa original"></div>
      </div>
      <div class="compare-panel">
        <div class="compare-panel-label"><span>Zoneamento gerado</span><span id="zone-count"></span></div>
        <div class="img-frame"><img id="img-zones" alt="Mapa de zonas classificado"></div>
      </div>
    </div>

    <div class="legend">
      <div class="legend-item"><span class="dot" style="background:#cf5147"></span> Baixa → dose +15%</div>
      <div class="legend-item"><span class="dot" style="background:#e0a83e"></span> Média → dose padrão</div>
      <div class="legend-item"><span class="dot" style="background:#4a9163"></span> Alta → dose −15%</div>
    </div>
  </section>

  <section class="section">
    <div class="section-num">02 — RESUMO</div>
    <h2>Painel da recomendação</h2>
    <p class="lead">Visão geral de quantas zonas caíram em cada categoria, para o índice selecionado.</p>

    <div class="kpi-strip" id="kpi-strip"></div>

    <div class="table-wrap">
      <div class="table-scroll">
        <table>
          <thead>
            <tr><th>Zona</th><th>Posição (linha, coluna)</th><th>Índice médio</th><th>Classificação</th><th>Dose recomendada</th></tr>
          </thead>
          <tbody id="table-body"></tbody>
        </table>
      </div>
    </div>
  </section>

  <footer><p>PROTÓTIPO — gerado automaticamente por gerar_prototipo.py</p></footer>
</div>

<script>
const DATA = __DATA_JSON__;
const indices = Object.keys(DATA).sort();
let current = indices[0];

function catClass(cat){ if(cat==='Baixa') return 'low'; if(cat==='Média') return 'mid'; return 'high'; }

function renderSelect(){
  const select = document.getElementById('index-select');
  select.innerHTML = indices.map(i => `<option value="${i}" ${i===current?'selected':''}>${DATA[i].label}</option>`).join('');
  select.onchange = (e) => { current = e.target.value; render(); };
}

function render(){
  const d = DATA[current];
  document.getElementById('img-orig').src = 'data:image/png;base64,' + d.orig;
  document.getElementById('img-zones').src = 'data:image/png;base64,' + d.zonemap;
  document.getElementById('label-orig').textContent = d.label;
  document.getElementById('zone-count').textContent = d.zonas.length + ' zonas';

  const counts = {Baixa:0, 'Média':0, Alta:0};
  d.zonas.forEach(z => counts[z.category]++);
  const avgDose = Math.round(d.zonas.reduce((a,z)=>a+z.dose_pct,0)/d.zonas.length);

  document.getElementById('kpi-strip').innerHTML = `
    <div class="kpi"><div class="kpi-label">Zonas — baixa</div><div class="kpi-value low">${counts.Baixa}</div></div>
    <div class="kpi"><div class="kpi-label">Zonas — média</div><div class="kpi-value mid">${counts['Média']}</div></div>
    <div class="kpi"><div class="kpi-label">Zonas — alta</div><div class="kpi-value high">${counts.Alta}</div></div>
    <div class="kpi"><div class="kpi-label">Dose média sugerida</div><div class="kpi-value">${avgDose}%</div></div>
  `;

  document.getElementById('table-body').innerHTML = d.zonas.map(z => `
    <tr>
      <td class="mono">Z-${String(z.id).padStart(2,'0')}</td>
      <td class="mono">(${z.row}, ${z.col})</td>
      <td class="mono">${z.avg_score}</td>
      <td><span class="badge ${catClass(z.category)}">${z.category}</span></td>
      <td class="mono">${z.dose_pct}%</td>
    </tr>
  `).join('');
}

renderSelect();
render();
</script>
</body>
</html>
"""


def gerar_html(pasta_entrada=PASTA_ENTRADA, arquivo_saida=ARQUIVO_SAIDA, escala=ESCALA_PADRAO):
    datasets = montar_datasets(pasta_entrada, escala)
    if not datasets:
        return

    html = TEMPLATE.replace("__DATA_JSON__", json.dumps(datasets, ensure_ascii=False))
    html = html.replace("__QTD_INDICES__", str(len(datasets)))

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nPronto! Abra o arquivo: {arquivo_saida}")


if __name__ == "__main__":
    gerar_html()
