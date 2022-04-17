var wtokuapi = false;

$(document).ready(function () {
    $("#livebox").on("input", function (e) {
        if (!wtokuapi) {
            wtokuapi = true;
            $("#datalist").empty();
            $.ajax({
                method: "post",
                url: "/search",
                data: { nazwa_uzytkownika: $("#livebox").val() },
                success: function (res) {
                    // var data = "<ul>";
                    // data += "<li>" + res + "</li>";
                    // data += "</ul>";
                    // $("#datalist").html(data);
                    console.log(res);
                },
            });
            wtokuapi = false;
        }
    });
});
