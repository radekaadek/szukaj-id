function loadingScreen() {
  $(window).on("load", function () {
      $(".loader-wrapper").fadeOut("slow");
  });
}

$(document).ready(() => {
  document.querySelector("#poleTxt").addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
          window.location.replace("../" + $("#poleTxt").val());
          $(".loader-wrapper").fadeIn("slow");
      }
  });
  loadingScreen();
});
