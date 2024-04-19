// Função para animar o texto como se estivesse sendo digitado
window.onload = function() {
    const effectText = document.getElementById('effectText');
    const subText = document.getElementById('subText');
    const subTextContent = "          sua insatisfação em ação"; // Adicionando espaços para igualar o comprimento
    const textToType = "Transforme";
    let index = 0;
  
    function typeWriter() {
      if (index < textToType.length) {
        effectText.innerHTML += textToType.charAt(index);
        index++;
        setTimeout(typeWriter, 100); // Tempo entre cada letra (em milissegundos)
      } else {
        setTimeout(function() {
          typeSubText();
          subText.style.transition = "opacity 1s ease-in-out";
          subText.style.opacity = "1";
        }, 500);
      }
    }
  
    function typeSubText() {
      let subIndex = 0;
      function type() {
        if (subIndex < subTextContent.length) {
          subText.innerHTML += subTextContent.charAt(subIndex);
          subIndex++;
          setTimeout(type, 100); // Tempo entre cada letra (em milissegundos)
        }
      }
      setTimeout(type, 500); // Espera 500ms antes de começar a digitar "em ação"
    }
  
    setTimeout(function() {
      typeWriter();
      effectText.style.transition = "opacity 1s ease-in-out";
      effectText.style.opacity = "1";
    }, 500);
  };
  
  // Script login
  const sign_in_btn = document.querySelector("#sign-in-btn");
  const sign_up_btn = document.querySelector("#sign-up-btn");
  const container = document.querySelector(".container");
  
  sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
  });
  
  sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
  });


function confirmarExclusao(id) {
      if (confirm("Tem certeza de que deseja excluir esta solicitação?")) {
          window.location.href = "/excluir/" + id;
      }
   }


    function mostrarFormResposta(id) {
        var formResposta = document.getElementById("formResposta" + id);
        // Verificar o estado atual do formulário
        if (formResposta.style.display === "none" || formResposta.style.display === "") {
            // Se estiver oculto, exibir o formulário
            formResposta.style.display = "block";
        } else {
            // Se estiver visível, ocultar o formulário
            formResposta.style.display = "none";
        }
    }
