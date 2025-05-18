const togglePasswordVisibility = (inputElement, toggleElement) => {
  if (inputElement.type === "password") {
    inputElement.type = "text";
    toggleElement.innerHTML = '<i class="fa fa-eye"></i>';
  } else {
    inputElement.type = "password";
    toggleElement.innerHTML = '<i class="fa fa-eye-slash"></i>';
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
