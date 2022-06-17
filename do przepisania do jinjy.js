const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`<div id="datalists_contaier" class="jsdom"></div>`);

inputObj = JSON.parse(process.argv[2].toString());
let favgamesplaytime = [];
// console.log(inputObj);

function rankCreator(input, newLI) {
    const rankContainer = dom.window.document.createElement('div');

    if (input.tier !== null && input.rank !== null && input.isLOL) {
        const rankImg = dom.window.document.createElement("img");
        const rankSpan = dom.window.document.createElement("span");
    
        rankImg.src = `../static/lolranks/${input.tier}.png`;
        rankImg.classList.add("tierImg");
        rankSpan.innerHTML = input.tier + input.rank;

        rankContainer.appendChild(rankImg);
        rankContainer.appendChild(rankSpan);
    }

    else if (input.isLOL){
        const mindBlownImg = dom.window.document.createElement("img");
        const infoSpan = dom.window.document.createElement("span");

        mindBlownImg.src = '../static/emoji_mindBlown.svg';
        mindBlownImg.classList.add("mindBlown");
        infoSpan.classList.add("infoSpan");
        infoSpan.innerHTML = "Chłop nie ma rangi";

        rankContainer.appendChild(mindBlownImg);
        rankContainer.appendChild(infoSpan);
    }

    rankContainer.classList.add("rankContainer");
    newLI.appendChild(rankContainer);
}

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

function avatar(input, newLI) {
    const urlLink = input.avatar;
    const profileAvatar = dom.window.document.createElement("a");
    profileAvatar.classList.add("profileAvatar");
    if (urlLink !== null) {
        profileAvatar.style.backgroundImage = `url(${urlLink})`;
        profileAvatar.href = urlLink;
    } else {
        profileAvatar.style.backgroundImage = "url(../static/happy_face.svg)";
    }

    profileAvatar.classList.add("avatarBorder");

    switch (input.status) {
        case 1:
            profileAvatar.classList.add("online");
            break;
        case 0:
            profileAvatar.classList.add("offline");
            break;
        case 2:
            profileAvatar.classList.add("busy");
            break;
        default:
            profileAvatar.classList.remove("avatarBorder");
    }
    
    newLI.appendChild(profileAvatar);
}

function gamelist(games) {
    const gameUL = dom.window.document.createElement("UL");
    gameUL.style.display = "inline-block";
    gameUL.classList.add("gamesList");
    for (const g in games) {
        const newGame = dom.window.document.createElement("LI");
        const nSpan = dom.window.document.createElement("span");
        const tSpan = dom.window.document.createElement("span");
        const gameIMG = dom.window.document.createElement("IMG");

        favgamesplaytime[Number(g) - 1] = games[g].playtime_forever;

        nSpan.innerHTML = g + ". " + games[g].name;
        gameIMG.src = `http://media.steampowered.com/steamcommunity/public/images/apps/${games[g].appid}/${games[g].img_icon_url}.jpg`;
        newGame.id = "game" + g;
        tSpan.classList.add("timeIndicator");
        tSpan.innerHTML = minutesToDhms(favgamesplaytime[Number(g) - 1]);
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
    const newLI = dom.window.document.createElement("li");

    avatar(input, newLI);

    if (('url' in input) && ('personaname' in input)) {
        const profileLink = dom.window.document.createElement("a");
        profileLink.innerHTML = input.personaname;
        profileLink.href = input.url;
        profileLink.classList.add("profileLink");
        newLI.appendChild(profileLink);
    }

    if (('favgames' in input)) {
        const games = gamelist(input.favgames);
        newLI.appendChild(games);
    }

    rankCreator(input, newLI); 

    if ('level' in input) {
        const level = dom.window.document.createElement("span");
        level.innerHTML = input.level;
        level.classList.add("levelIndicator");
        newLI.appendChild(level);
    }   

    return newLI;
}

async function crHtml(res) {
    const datalistContainerDiv = dom.window.document.querySelector("#datalists_contaier");;
    const newUL = dom.window.document.createElement("UL");
    for (const d in res) {
        if (res[d].error !== 'OK') {
            continue;
        }
        const logo = dom.window.document.createElement("img");
        const newLine = await newline(res[d]);

        newLine.id = d + "Line";
        logo.id = d + "Logo";
        newLine.classList.add("platformLine");
        logo.classList.add("platformLogo");
        logo.src = `../static/${d}_icon.svg`;

        newLine.appendChild(logo);
        newUL.appendChild(newLine);
    }
    datalistContainerDiv.appendChild(newUL);
    console.log(datalistContainerDiv.outerHTML);
}

crHtml(inputObj);