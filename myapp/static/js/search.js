document.addEventListener("DOMContentLoaded", function () {
  var searchIcon = document.getElementById("search-icon");
  var searchFormContainer = document.getElementById("search-form-container");

  searchIcon.addEventListener("click", function () {
    if (searchFormContainer.style.display === "none") {
      searchFormContainer.style.display = "block";
    } else {
      searchFormContainer.style.display = "none";
    }
  });
});
