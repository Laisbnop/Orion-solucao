
const form = document.getElementById("loginForm");
const inputUsuario = document.getElementById("usuario");
const inputSenha = document.getElementById("senha");
const botaoMostrarSenha = document.getElementById("toggleSenha");
const mensagemErro = document.getElementById("loginError");


botaoMostrarSenha.addEventListener("click", () => {
  const escondida = inputSenha.type === "password";
  inputSenha.type = escondida ? "text" : "password";
  botaoMostrarSenha.textContent = escondida ? "ocultar" : "mostrar";
});


const normalizar = (texto) => texto.replace(/\s+/g, "").toLowerCase();

form.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const usuario = normalizar(inputUsuario.value);
  const senha = normalizar(inputSenha.value);

  if (usuario === "" || senha === "") {
    mostrarErro("Preencha usuário e senha.");
    return;
  }

  const encontrado = USUARIOS.find((u) => u.login === usuario && u.senha === senha);
  if (!encontrado) {
    mostrarErro("Usuário ou senha inválidos.");
    return;
  }

  esconderErro();

  const { nome, papel, fazenda } = encontrado;
  sessionStorage.setItem("usuario", JSON.stringify({ nome, papel, fazenda }));
  window.location.href = "painel.html";
});

function mostrarErro(texto) {
  mensagemErro.textContent = texto;
  mensagemErro.hidden = false;
}

function esconderErro() {
  mensagemErro.hidden = true;
}