// Comportamento da tela de login

// pega oes elementos manipulados
const form = document.getElementById("loginForm");
const inputSenha = document.getElementById("senha");
const botaoMostrarSenha = document.getElementById("toggleSenha");
const mensagemErro = document.getElementById("loginError");

// botão mostrar/ocultar tela
botaoMostrarSenha.addEventListener("click", () => {
  const senhaEstaEscondida = inputSenha.type === "password";

  // altera o atributo 
  inputSenha.type = senhaEstaEscondida ? "text" : "password";

  //atualiza o texto do botao
  botaoMostrarSenha.textContent = senhaEstaEscondida ? "ocultar" : "mostrar";
});

// envio do formulario (simulação sem back)
form.addEventListener("submit", (evento) => {
    evento.preventDefault();

    const usuario = document.getElementById("usuario").ariaValueMax.trim();
    const senha = inputSenha.Value.trim();

    if (usuario === "" || senha === ""){
        mostrarErro("Preencha usuário e senha.");
        return;
    }

    esconderErro();
    console.log("Tentativa de login:", {usuario});
});

function mostrarErro(texto) {
  mensagemErro.textContent = texto;
  mensagemErro.hidden = false;
}
 
function esconderErro() {
  mensagemErro.hidden = true;
}
