

const sessao = JSON.parse(sessionStorage.getItem("usuario"));
if (!sessao) window.location.href = "index.html"; 

const ehOrion = sessao.papel === "orion";
const conteudo = document.getElementById("conteudo");

const STATUS = {
  ok:     { texto: "Dentro do esperado", cor: "green" },
  abaixo: { texto: "Abaixo do esperado", cor: "orange" },
  acima:  { texto: "Acima do esperado",  cor: "red" }
};

const MENUS = {
  orion:    [["visao", "Visão geral"], ["produtores", "Produtores"], ["alertas", "Alertas"]],
  produtor: [["visao", "Visão geral"], ["fazenda", "Minha fazenda"], ["alertas", "Alertas"]]
};



const cabecalho = (titulo, subtitulo, info = "") => `
  <header class="page-head">
    <div><h1>${titulo}</h1><p>${subtitulo}</p></div>
    <span class="page-head__info">${info}</span>
  </header>`;

const card = (rotulo, valor, cor = "") =>
  `<div class="stat"><span>${rotulo}</span><strong class="txt-${cor}">${valor}</strong></div>`;

const selo = (situacao) =>
  `<span class="badge badge--${STATUS[situacao].cor}">● ${STATUS[situacao].texto}</span>`;

const chips = (lista) => lista.map(([valor, texto], i) =>
  `<button class="chip${i === 0 ? " ativo" : ""}" data-filtro="${valor}">${texto}</button>`).join("");



const paginas = {
  visao() {
    const alertas = ehOrion ? ALERTAS : ALERTAS.filter((a) => a.fazenda === sessao.fazenda);
    const cards = ehOrion
      ? card("Produtores", 20) + card("Fazendas", 34) + card("Talhões", 287)
      : card("Talhões", FAZENDA.talhoes) + card("Área total", FAZENDA.area + " ha") + card("Aplicações", 58);

    return cabecalho("Visão geral", ehOrion ? "Todos os produtores" : "Fazenda " + FAZENDA.nome, "Atualizado em 31/08/2026")
      + `<div class="stats">${cards}${card("Alertas ativos", alertas.length, "green")}</div>
         <div class="painel vazio">Dashboard — em desenvolvimento</div>`;
  },

  produtores() {
    return cabecalho("Produtores", "", "20 produtores cadastrados")
      + `<div class="filtros">
           <input id="busca" placeholder="Buscar produtor...">
           ${chips([["todos", "Todos"], ["ok", "Regular"], ["abaixo", "Atenção"], ["acima", "Alerta"]])}
         </div>
         <div id="lista"></div>`;
  },

  fazenda() {
    const resumo = Object.entries(FAZENDA.resumo).map(([chave, qtd]) =>
      `<div class="stat"><span class="badge-texto"><i class="dot dot--${STATUS[chave].cor}"></i> ${STATUS[chave].texto}</span>
       <strong class="txt-${STATUS[chave].cor}">${qtd}</strong><small>aplicações</small></div>`).join("");

    const talhoes = TALHOES.map((t) =>
      `<button class="talhao"><b>${t.id}</b><i class="dot dot--${STATUS[t.status].cor}"></i></button>`).join("");

    return cabecalho("Minha fazenda", "Fazenda " + FAZENDA.nome, "Última atualização: 31/08/2026")
      + `<div class="painel">
           <p class="rotulo">FAZENDA ${FAZENDA.nome.toUpperCase()}</p>
           <p>Produtor: ${FAZENDA.produtor}</p>
           <p>Área total: <b>${FAZENDA.area} ha</b> · Talhões: <b>${FAZENDA.talhoes}</b> · Aplicações recentes: <b>${FAZENDA.recentes}</b></p>
         </div>
         <div class="stats">${resumo}</div>
         <h2>Talhões</h2>
         <div class="talhoes">${talhoes}</div>`;
  },

  alertas() {
    const alertas = ehOrion ? ALERTAS : ALERTAS.filter((a) => a.fazenda === sessao.fazenda);
    const aviso = ehOrion ? `<div class="aviso">⚠ <b>3 produtores</b> apresentam desvios recorrentes nos últimos 30 dias.</div>` : "";
    return cabecalho("Alertas", "", alertas.length + " ocorrências precisam de atenção")
      + `<div class="filtros">${chips([["todos", "Todos"], ["abaixo", "Abaixo"], ["acima", "Acima"], ["recorrente", "Recorrentes"]])}</div>`
      + aviso + `<div id="lista"></div>`;
  },

  config() {
    return cabecalho("Configurações", "") + `<div class="painel vazio">Em desenvolvimento</div>`;
  }
};



function desenharProdutores(filtro, termo) {
  const lista = PRODUTORES.filter((p) =>
    (filtro === "todos" || p.situacao === filtro) && (p.nome + p.fazenda).toLowerCase().includes(termo));

  document.getElementById("lista").innerHTML = `
    <table>
      <tr><th>Produtor</th><th>Fazenda</th><th>Talhões</th><th>Situação</th></tr>
      ${lista.map((p) => `<tr><td><b>${p.nome}</b></td><td>${p.fazenda}</td><td>${p.talhoes}</td><td>${selo(p.situacao)}</td></tr>`).join("")}
    </table>`;
}

function desenharAlertas(filtro) {
  const base = ehOrion ? ALERTAS : ALERTAS.filter((a) => a.fazenda === sessao.fazenda);
  const lista = base.filter((a) => filtro === "todos" || a.tipo === filtro || (filtro === "recorrente" && a.recorrente));

  document.getElementById("lista").innerHTML = lista.map((a) => `
    <article class="alerta alerta--${STATUS[a.tipo].cor}">
      <div><b>${a.talhao}</b> <span>Fazenda ${a.fazenda}</span><p>${a.texto}</p><small>${a.data}</small></div>
      <button class="btn-outline">Ver aplicação</button>
    </article>`).join("") || `<p class="vazio">Nenhum alerta neste filtro.</p>`;
}


function ligarFiltros(desenhar) {
  const busca = document.getElementById("busca");
  let filtro = "todos";
  const atualizar = () => desenhar(filtro, busca ? busca.value.toLowerCase() : "");

  document.querySelectorAll(".chip").forEach((chip) => chip.addEventListener("click", () => {
    document.querySelector(".chip.ativo").classList.remove("ativo");
    chip.classList.add("ativo");
    filtro = chip.dataset.filtro;
    atualizar();
  }));
  if (busca) busca.addEventListener("input", atualizar);
  atualizar();
}

const aoAbrir = {
  produtores: () => ligarFiltros(desenharProdutores),
  alertas: () => ligarFiltros(desenharAlertas)
};



function abrir(pagina) {
  conteudo.innerHTML = paginas[pagina]();
  document.querySelectorAll(".sidebar button[data-pagina]").forEach((b) =>
    b.classList.toggle("ativo", b.dataset.pagina === pagina));
  if (aoAbrir[pagina]) aoAbrir[pagina]();
}

document.getElementById("perfil").textContent = ehOrion ? "Agrônomo · Colaborador" : "Portal do Produtor";
document.getElementById("nomeUsuario").textContent = sessao.nome;
document.getElementById("papelUsuario").textContent = ehOrion ? "Agrônomo" : "Produtor";
document.getElementById("avatar").textContent = sessao.nome.replace("Dr. ", "")[0];
document.getElementById("menu").innerHTML = MENUS[sessao.papel]
  .map(([id, nome]) => `<button data-pagina="${id}">${nome}</button>`).join("");

document.querySelector(".sidebar").addEventListener("click", (e) => {
  if (e.target.dataset.pagina) abrir(e.target.dataset.pagina);
});
document.getElementById("sair").addEventListener("click", () => {
  sessionStorage.removeItem("usuario");
  window.location.href = "index.html";
});

abrir("visao");