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
                        if (res !== 'ZAMKOR'){
                        $("#attentionMessage").css({ display: "none" })    
                        var data = "<ul>";
                        data += "<li>" + JSON.stringify(res) + "</li>";
                        data += "</ul>";
                        $("#datalist").html(data);
                        console.log(res);}
                        else $("#attentionMessage").css({ display: "block" })
                    },
                });
                wtokuapi = false;
            }, 500);
        }
    });
});
