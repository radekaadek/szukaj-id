$(document).ready(function () {
    $("#livebox").on("input", function (e) {
        $("#datalist").empty();
        $.ajax({
            method: "post",
            url: "/search",
            data: { nazwa_uzytkownika: $("#livebox").val() },
            success: function (res) {
                if (res.length > 0) {
                    var data = "<ul>";
                    data += "<li>" + res + "</li>";
                    data += "</ul>";
                    $("#datalist").html(data);
                    console.log(res);
                }
            },
        });
    });
});