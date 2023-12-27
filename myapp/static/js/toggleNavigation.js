function toggleNavigation() {
  var navMenu = document.getElementById("navbarSupportedContent");
  var toggleButton = document.querySelector(".navbar-toggler");

  function updateNavDisplay() {
    if (window.innerWidth <= 768) {
      navMenu.style.display = "none";
    } else {
      navMenu.style.display = "block";
    }
  }

  updateNavDisplay();

  toggleButton.addEventListener("click", function () {
    if (navMenu.style.display === "none") {
      navMenu.style.display = "block";
    } else {
      navMenu.style.display = "none";
    }
  });

  window.addEventListener("resize", updateNavDisplay);
}
toggleNavigation();
