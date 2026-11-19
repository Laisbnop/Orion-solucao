var PAGINA_PAINEL = "painel.html";  
var LIMITE_TENTATIVAS = 3;
var TEMPO_BLOQUEIO = 60;             

var form = document.getElementById("loginForm");
var inputUsuario = document.getElementById("usuario");
var inputSenha = document.getElementById("senha");
var checkLembrar = document.getElementById("lembrar");
var botaoMostrar = document.getElementById("toggleSenha");
var botaoEntrar = document.getElementById("btnEntrar");
var mensagemErro = document.getElementById("loginError");
var mensagemSucesso = document.getElementById("loginSucesso");

var tentativas = 0;
var bloqueadoAte = 0;

try {
  var salvo = localStorage.getItem("orion_usuario");
  if (salvo) {
    inputUsuario.value = salvo;
    checkLembrar.checked = true;
    inputSenha.focus();
  }
} catch (erro) {
}

botaoMostrar.addEventListener("click", function () {
  if (inputSenha.type == "password") {
    inputSenha.type = "text";
    botaoMostrar.innerText = "Ocultar";
  } else {
    inputSenha.type = "password";
    botaoMostrar.innerText = "Mostrar";
  }
});

function normalizar(texto) {
  return texto.replace(/\s+/g, "").toLowerCase();
}

function fazerLogin(usuario, senha) {
  for (var i = 0; i < USUARIOS.length; i++) {
    if (USUARIOS[i].login == usuario) {
      if (USUARIOS[i].senha != senha) {
        return { sucesso: false, motivo: "Senha incorreta." };
      }
      return { sucesso: true, dados: USUARIOS[i] };
    }
  }
  return { sucesso: false, motivo: "Usuário não encontrado." };
}

function mostrarErro(texto) {
  mensagemSucesso.innerText = "";
  mensagemErro.innerText = texto;
}

form.addEventListener("submit", function (evento) {
  evento.preventDefault();
  mensagemErro.innerText = "";
  mensagemSucesso.innerText = "";

  var usuario = normalizar(inputUsuario.value);
  var senha = normalizar(inputSenha.value);

  if (usuario == "" || senha == "") {
    mostrarErro("Preencha usuário e senha.");
    return;
  }

  var agora = new Date().getTime();
  if (agora < bloqueadoAte) {
    var segundos = Math.ceil((bloqueadoAte - agora) / 1000);
    mostrarErro("Muitas tentativas erradas. Tente de novo em " + segundos + "s.");
    return;
  }

  botaoEntrar.disabled = true;
  botaoEntrar.innerText = "Entrando...";

  setTimeout(function () {
    botaoEntrar.disabled = false;
    botaoEntrar.innerText = "Entrar";

    var login = fazerLogin(usuario, senha);

    if (!login.sucesso) {
      tentativas++;
      var restantes = LIMITE_TENTATIVAS - tentativas;
      if (restantes <= 0) {
        bloqueadoAte = new Date().getTime() + TEMPO_BLOQUEIO * 1000;
        tentativas = 0;
        mostrarErro("Muitas tentativas erradas. Acesso bloqueado por 1 minuto.");
      } else {
        mostrarErro(login.motivo + " Restam " + restantes + " tentativa(s).");
      }
      return;
    }

    tentativas = 0;

    try {
      if (checkLembrar.checked) {
        localStorage.setItem("orion_usuario", usuario);
      } else {
        localStorage.removeItem("orion_usuario");
      }
      var pessoa = { nome: login.dados.nome, papel: login.dados.papel, fazenda: login.dados.fazenda };
      sessionStorage.setItem("usuario", JSON.stringify(pessoa));
    } catch (erro) {
    }

    mensagemSucesso.innerText = "Login realizado! Bem-vindo(a), " + login.dados.nome + ".";
    setTimeout(function () {
      window.location.href = PAGINA_PAINEL;
    }, 1000);
  }, 500);
});
