var wtokuapi = false;
let favgamesplaytime = [];

function gamelist(games){
    const gameUL = document.createElement("UL");
    for (const g in games) {
        const newGame = document.createElement("LI");
        const nSpan = document.createElement("span");
        const gameIMG = document.createElement("IMG")

        nSpan.innerText = g + ". " + games.name;
        gameIMG.scr = ""

        newGame.id = "game" + g;
        gameUL.appendChild(newGame);
    }
}

function newline(input) {
    const newLI = document.createElement("li");
    const profileAvatar = document.createElement("a");
    const profileLink = document.createElement("a")
    
    profileLink.innerText = input.personaname
    profileLink.href = input.url
    profileLink.classList.add('profile-link');

    profileAvatar.style.backgroundImage = `url(${input.avatar})`;
    profileAvatar.style.width = "100px";
    profileAvatar.style.backgroundSize = "100px 100px";
    profileAvatar.style.height = "100px";
    profileAvatar.style.display = "inline-block";
    profileAvatar.href = input.avatar;


    newLI.appendChild(gamelist(input.favgames));
    newLI.appendChild(profileAvatar);
    newLI.appendChild(profileLink);
    
    return newLI;
}

function crHtml(res) {
    const datalistContainerDiv = document.querySelector("body #datalists_contaier");
    datalistContainerDiv.innerHTML = "";
    const newUL = document.createElement("UL");
    for (const d in res) {
        const newLine = newline(res[d]);
        newLine.id = d + "Line"
        newUL.appendChild(newLine);
    }
    datalistContainerDiv.appendChild(newUL);
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
                        else {
                            $("#attentionMessage").css({ display: "block" })
                            $("#datalists_contaier").empty();
                        }
                    },
                });
                wtokuapi = false;
            }, 500);
        }
    });
});