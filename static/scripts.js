{let loadingScreen = function () {
  $(window).on("load", function () {
      $(".loader-wrapper").fadeOut("slow");
  });
}

let redirFu = function () {
      window.location.replace("../" + $("#webSearchInput").val());
      $(".loader-wrapper").fadeIn("slow");
}

// Search Bar
$(document).ready(() => {
  document.querySelector("#webSearchInput").addEventListener("keypress",(e)=>{
    if (e.key === "Enter") {
        redirFu();
    }
});

  document.querySelector(".web-search-submit").addEventListener("click", redirFu);
  loadingScreen();
});
}
