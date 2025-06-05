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
<script>
  const images = document.querySelectorAll(".carousel-image");
  const prevBtn = document.querySelector(".prev");
  const nextBtn = document.querySelector(".next");
  let current = 0;

  function updateCarousel() {
    images.forEach((img, index) => {
      img.classList.toggle("active", index === current);
    });
  }

  prevBtn.addEventListener("click", () => {
    current = (current - 1 + images.length) % images.length;
    updateCarousel();
  });

  nextBtn.addEventListener("click", () => {
    current = (current + 1) % images.length;
    updateCarousel();
  });

  // Optional: Swipe support for mobile
  let startX;
  document.querySelector(".carousel-container").addEventListener("touchstart", (e) => {
    startX = e.touches[0].clientX;
  });

  document.querySelector(".carousel-container").addEventListener("touchend", (e) => {
    let endX = e.changedTouches[0].clientX;
    if (startX - endX > 50) nextBtn.click(); // Swipe Left
    else if (endX - startX > 50) prevBtn.click(); // Swipe Right
  });

  updateCarousel(); // Initial display
</script>
