var wtokuapi = false;
let favgamesplaytime = [];

function gamelist(games) {
    const gameUL = document.createElement("UL");
    gameUL.style.display = "inline-block";
    for (const g in games) {
        const newGame = document.createElement("LI");
        const nSpan = document.createElement("span");
        const gameIMG = document.createElement("IMG");

        nSpan.innerText = g + ". " + games[g].name;
        gameIMG.src = `http://media.steampowered.com/steamcommunity/public/images/apps/${games[g].appid}/${games[g].img_icon_url}.jpg`;
        newGame.id = "game" + g;
        newGame.appendChild(gameIMG);
        newGame.appendChild(nSpan);

        gameUL.appendChild(newGame);
    }
    return gameUL;
}

function newline(input) {
    const newLI = document.createElement("li");
    const profileAvatar = document.createElement("a");
    const profileLink = document.createElement("a");
    const games = gamelist(input.favgames);

    profileLink.innerText = input.personaname;
    profileLink.href = input.url;
    profileLink.classList.add("profile-link");

    profileAvatar.style.backgroundImage = `url(${input.avatar})`;
    profileAvatar.style.width = "100px";
    profileAvatar.style.backgroundSize = "100px 100px";
    profileAvatar.style.height = "100px";
    profileAvatar.style.display = "inline-block";
    profileAvatar.href = input.avatar;

    newLI.appendChild(profileAvatar);
    newLI.appendChild(profileLink);
    newLI.appendChild(games);

    return newLI;
}

function crHtml(res) {
    const datalistContainerDiv = document.querySelector("body #datalists_contaier");
    datalistContainerDiv.innerHTML = "";
    const newUL = document.createElement("UL");
    for (const d in res) {
        if (res[d] == null) {
            continue;
        }
        const newLine = newline(res[d]);
        newLine.id = d + "Line";
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
                        if (res !== "ZAMKOR") {
                            $("#attentionMessage").css({ display: "none" });
                            crHtml(res);
                            console.log(res);
                        } else {
                            $("#attentionMessage").css({ display: "block" });
                            $("#datalists_contaier").empty();
                        }
                    },
                });
                wtokuapi = false;
            }, 500);
        }
    });
});
