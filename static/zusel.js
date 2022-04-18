var wtokuapi = false;


function crHtml(res) {
    const datalistContainerDiv = document.querySelector("body #datalists_contaier");
    for (const d in res) {
        const newUL = document.createElement("UL");
        for (const r in res[d]) {
            const newLI = document.createElement("li");
            newLI.innerText = JSON.stringify(res[d][r]);
            newUL.appendChild(newLI);
        }
        newUL.id = d + "List"
        datalistContainerDiv.appendChild(newUL);
    }

}

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
                        crHtml(res);
                        console.log(res);}
                        else $("#attentionMessage").css({ display: "block" })
                    },
                });
                wtokuapi = false;
            }, 500);
        }
    });
});