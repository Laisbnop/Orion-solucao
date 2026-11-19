// Dados de exemplo (simulam o back-end). 

const USUARIOS = [
  { login: "agronomo1", senha: "orion123", nome: "Dr. Carlos Mendes", papel: "orion" },
  { login: "fazenda1",  senha: "santaluzia123", nome: "João Silva", papel: "produtor", fazenda: "Santa Luzia" }
];

const PRODUTORES = [
  { nome: "João Silva",     fazenda: "Santa Luzia", talhoes: 20, situacao: "ok" },
  { nome: "Maria Santos",   fazenda: "Boa Vista",   talhoes: 15, situacao: "abaixo" },
  { nome: "Carlos Oliveira",fazenda: "São José",    talhoes: 18, situacao: "acima" },
  { nome: "Ana Lima",       fazenda: "Três Irmãos", talhoes: 12, situacao: "ok" },
  { nome: "Rodrigo Mendes", fazenda: "Campo Novo",  talhoes: 24, situacao: "abaixo" },
  { nome: "Fernanda Costa", fazenda: "Bela Manhã",  talhoes: 9,  situacao: "ok" },
  { nome: "Paulo Sousa",    fazenda: "Rio Verde",   talhoes: 31, situacao: "ok" },
  { nome: "Luciana Braga",  fazenda: "Alto Sertão", talhoes: 14, situacao: "acima" }
];

const ALERTAS = [
  { talhao: "T02", fazenda: "Santa Luzia", tipo: "abaixo", texto: "Aplicação 20% abaixo do esperado.", data: "30/08/2026", recorrente: true },
  { talhao: "T08", fazenda: "Boa Vista",   tipo: "acima",  texto: "Aplicação 31% acima do esperado.",  data: "29/08/2026", recorrente: true },
  { talhao: "T04", fazenda: "São José",    tipo: "acima",  texto: "Aplicação 28% acima do esperado.",  data: "28/08/2026", recorrente: true },
  { talhao: "T11", fazenda: "Santa Luzia", tipo: "abaixo", texto: "Aplicação 14% abaixo do esperado.", data: "27/08/2026", recorrente: false },
  { talhao: "T07", fazenda: "Campo Novo",  tipo: "abaixo", texto: "Aplicação 17% abaixo do esperado.", data: "26/08/2026", recorrente: false },
  { talhao: "T09", fazenda: "Alto Sertão", tipo: "acima",  texto: "Aplicação 12% acima do esperado.",  data: "25/08/2026", recorrente: false }
];


const FAZENDA = { nome: "Santa Luzia", produtor: "João Silva", area: 250, talhoes: 20, recentes: 8,
                  resumo: { ok: 12, abaixo: 4, acima: 2 } };

const TALHOES = [
  ["T01","ok"],["T02","abaixo"],["T03","ok"],["T04","acima"],["T05","ok"],["T06","ok"],
  ["T07","abaixo"],["T08","ok"],["T09","ok"],["T10","ok"],["T11","abaixo"],["T12","ok"]
].map(([id, status]) => ({ id, status }));