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


  const formulario = document.getElementById('formulario');
  const username = document.getElementById('username');
  const email = document.getElementById('email');
  const senha = document.getElementById('senha');
  const confirmaSenha = document.getElementById('confirma_senha');
  
  formulario.addEventListener('submit', (e) => {
      e.preventDefault();
  
      checkInputs();
  });
  
  function checkInputs() {
      const usernameValue = username.value.trim();
      const emailValue = email.value.trim();
      const senhaValue = senha.value.trim();
      const confirmaSenhaValue = confirmaSenha.value.trim();
  
      if(usernameValue === '') {
          setErrorFor(username, 'Username cannot be blank');
      } else {
          setSuccessFor(username);
      }
  
      if(emailValue === '') {
          setErrorFor(email, 'Email cannot be blank');
      } else if (!isEmail(emailValue)) {
          setErrorFor(email, 'Not a valid email');
      } else {
          setSuccessFor(email);
      }
  
      if(senhaValue === '') {
          setErrorFor(senha, 'Password cannot be blank');
      } else {
          setSuccessFor(senha);
      }
  
      if(confirmaSenhaValue === '') {
          setErrorFor(confirmaSenha, 'Password confirmation cannot be blank');
      } else if(senhaValue !== confirmaSenhaValue) {
          setErrorFor(confirmaSenha, 'Passwords do not match');
      } else {
          setSuccessFor(confirmaSenha);
      }
  
      // If all inputs are valid, submit the form
      if(usernameValue !== '' && emailValue !== '' && isEmail(emailValue) && senhaValue !== '' && confirmaSenhaValue !== '' && senhaValue === confirmaSenhaValue) {
          enviarDados();
      }
  }
  
  function setErrorFor(input, message) {
      const formControl = input.parentElement;
      const small = formControl.querySelector('small');
  
      // Add error message inside small
      small.innerText = message;
  
      // Add error class
      formControl.className = 'input-field error';
  }
  
  function setSuccessFor(input) {
      const formControl = input.parentElement;
      formControl.className = 'input-field success';
  }
  
  function isEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
  
  function enviarDados() {
      const formData = new FormData(formulario);
  
      fetch('/cadastrar', {
          method: 'POST',
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          if(data.message) {
              alert(data.message);
              formulario.reset();
              window.location.href = '/login'; // Redireciona para a página de login após o cadastro bem-sucedido
          } else {
              alert('Erro ao cadastrar usuário.');
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
  }
  
  // botton ADM

  function mostrarChaveAcesso() {
    var chaveAcessoField = document.getElementById("chaveAcessoField");
    var passwordField = document.getElementById("password");

    if (chaveAcessoField.style.display === "none") {
        chaveAcessoField.style.display = "block";
        passwordField.style.marginBottom = "10px"; // Ajuste de estilo opcional
    } else {
        chaveAcessoField.style.display = "none";
        passwordField.style.marginBottom = ""; // Limpa o ajuste de estilo
    }
}