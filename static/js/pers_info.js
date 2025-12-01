document.getElementById("contactForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const msg = document.getElementById("successMessage");
  msg.style.display = "block";
  this.reset();
  setTimeout(() => msg.style.display = "none", 3000);
});