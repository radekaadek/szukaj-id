var wtokuapi = false;
let favgamesplaytime = [];

function minutesToDhms(seconds) {
    seconds = Number(seconds);
    seconds = seconds * 60;
    var d = Math.floor(seconds / (3600 * 24));
    var h = Math.floor((seconds % (3600 * 24)) / 3600);
    var m = Math.floor((seconds % 3600) / 60);

    var dDisplay = d > 0 ? d + (d == 1 ? " day, " : " days, ") : "";
    var hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " hours, ") : "";
    var mDisplay = m > 0 ? m + (m == 1 ? " minute " : " minutes ") : "";
    return dDisplay + hDisplay + mDisplay;
}

async function avatar(input, newLI) {
    const urlLink = input.avatar;
    const profileAvatar = document.createElement("a");
    profileAvatar.classList.add("profileAvatar");
    let exists = false;

    await $.ajax({
        type: "HEAD",
        url: urlLink,
        success: () => {
            exists = true;
        }
    }).catch(() => {
        console.log("O ja cie w ten czas");
    });;

    if (urlLink !== null && exists) {
        profileAvatar.style.backgroundImage = `url(${urlLink})`;
        profileAvatar.href = urlLink;
    } else {
        profileAvatar.style.backgroundImage = "url(../static/happy_face.svg)";
    }

    profileAvatar.style.width = "180px";
    profileAvatar.style.backgroundSize = "180px 180px";
    profileAvatar.style.height = "180px";
    profileAvatar.style.display = "inline-block";
    newLI.appendChild(profileAvatar);
}

function gamelist(games) {
    const gameUL = document.createElement("UL");
    gameUL.style.display = "inline-block";
    gameUL.classList.add("gamesList");
    for (const g in games) {
        const newGame = document.createElement("LI");
        const nSpan = document.createElement("span");
        const tSpan = document.createElement("span");
        const gameIMG = document.createElement("IMG");

        favgamesplaytime[Number(g) - 1] = games[g].playtime_forever;

        nSpan.innerText = g + ". " + games[g].name;
        gameIMG.src = `http://media.steampowered.com/steamcommunity/public/images/apps/${games[g].appid}/${games[g].img_icon_url}.jpg`;
        newGame.id = "game" + g;
        tSpan.classList.add("timeIndicator");
        tSpan.innerText = favgamesplaytime[Number(g) - 1] + " minutes";
        tSpan.id = "time" + g;
        newGame.appendChild(gameIMG);
        newGame.appendChild(nSpan);
        newGame.appendChild(tSpan);
        newGame.classList.add("gameLine");

        gameUL.appendChild(newGame);
    }
    return gameUL;
}

async function newline(input) {
    const newLI = document.createElement("li");

    await avatar(input, newLI);

    if (input.url !== null && input.personaname !== null) {
        const profileLink = document.createElement("a");
        profileLink.innerText = input.personaname;
        profileLink.href = input.url;
        profileLink.classList.add("profileLink");
        newLI.appendChild(profileLink);
    }

    if (input.favgames !== null) {
        const games = gamelist(input.favgames);
        newLI.appendChild(games);
    }

    if (input.url !== null) {
        const level = document.createElement("span");
        level.innerText = input.level;
        level.classList.add("levelIndicator");
        newLI.appendChild(level);
    }

    if (input.tier !== null && input.rank !== null){
        const rankContainer = document.createElement('div')
        const rankImg = document.createElement("img")
        const rankSpan = document.createElement("span")

        rankContainer.classList.add("rankContainer");
        rankImg.src = `../static/lolranks/${input.tier}.png`;
        rankImg.classList.add("tierImg");
        rankSpan.innerText = input.tier + input.rank;

        rankContainer.appendChild(rankImg)
        rankContainer.appendChild(rankSpan)
        newLI.appendChild(rankContainer)
    }    

    return newLI;
}

async function crHtml(res) {
    const datalistContainerDiv = document.querySelector("body #datalists_contaier");
    datalistContainerDiv.innerHTML = "";
    const newUL = document.createElement("UL");
    for (const d in res) {
        if (res[d] == null) {
            continue;
        }
        const newLine = await newline(res[d]);
        newLine.id = d + "Line";
        newUL.appendChild(newLine);
    }
    datalistContainerDiv.appendChild(newUL);
}

function zamienCzas() {
    for (i = 1; i <= 3; i++) {
        document.getElementById("time" + i).innerText = minutesToDhms(favgamesplaytime[i - 1]);
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
                    success: async function (res) {
                        if (res !== "ZAMKOR") {
                            $("#attentionMessage").css({ display: "none" });
                            await crHtml(res);
                            console.log(res);
                        } else {
                            $("#attentionMessage").css({ display: "block" });
                            $("#datalists_contaier").empty();
                        }
                    },
                });
                wtokuapi = false;
            }, 750);
        }
    });
});