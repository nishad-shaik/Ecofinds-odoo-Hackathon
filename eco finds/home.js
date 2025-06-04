const togglePasswordVisibility = (inputElement, toggleElement) => {
  const icon = toggleElement.querySelector("i");
  if (inputElement.type === "password") {
    inputElement.type = "text";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  } else {
    inputElement.type = "password";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  }
};

const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");
const passwordConfirm = document.getElementById("passwordConfirm");
const togglePasswordConfirm = document.getElementById("togglePasswordConfirm");

togglePassword.addEventListener("click", () => {
  togglePasswordVisibility(passwordInput, togglePassword);
});

togglePasswordConfirm.addEventListener("click", () => {
  togglePasswordVisibility(passwordConfirm, togglePasswordConfirm);
});

// Submit handler
document.querySelector(".form").addEventListener("submit", function (e) {
  e.preventDefault();

  // Clear all inputs
  const inputs = document.querySelectorAll("input");
  inputs.forEach((input) => {
    input.value = "";
  });

  // Show toast
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerText = "Registration successful!";
  document.body.appendChild(toast);

  // Remove after 3 seconds
  setTimeout(() => {
    toast.remove();
  }, 3000);
});

document.addEventListener("DOMContentLoaded", function () {
    const exploreButton = document.querySelector("#hero button");
    exploreButton.addEventListener("click", function () {
        alert("Welcome to ECOFINDS!");
    });
});