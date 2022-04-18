var wtokuapi = false;

$(document).ready(async function () {
    $("#livebox").on("input", async function (e) {
        if (wtokuapi === false) {
            wtokuapi = true;
            $("#datalist").empty();
            setTimeout(() => {
                $.ajax({
                    method: "post",
                    url: "/search",
                    data: { nazwa_uzytkownika: $("#livebox").val() },
                    success: function (res) {
                        var data = "<ul>";
                        data += "<li>" + res + "</li>";
                        data += "</ul>";
                        $("#datalist").html(data);
                        console.log(res);
                    },
                });
                wtokuapi = false;
            }, 500);
        }
    });
});
