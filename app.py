from flask import Flask, render_template, request
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
from steamwebapi import profiles
import json, operator

app = Flask(__name__)
sortkey= operator.itemgetter('playtime_forever')
steam_api_key = 'EE03692ACB03E4371522180E26926643'
riot_api_key = 'RGAPI-872636ab-9da1-4355-8afa-a1ab624dd6f4'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods = ["POST", "GET"])
def search():
    #dokumentacja: https://pypi.org/project/steamwebapi/
    nazwa_uzytkownika = request.form["nazwa_uzytkownika"]

    #deklaracje głównych interfejsów API steam
    steamuserinfo = ISteamUser(steam_api_key = steam_api_key) 
    steamplayerinfo = IPlayerService(steam_api_key = steam_api_key)
    steamstatsinfo = ISteamUserStats(steam_api_key = steam_api_key)
    
    if len(nazwa_uzytkownika) > 0:
        #api request by pozyskać steam ID
        steamid = steamuserinfo.resolve_vanity_url(str(nazwa_uzytkownika), format="json")['response']['steamid']

        #api request by pozyskać dane w obiektach
        steamgamesinfo = steamplayerinfo.get_owned_games(steamid, format="json")['response']
        usersummary = steamuserinfo.get_player_summaries(steamid, format="json")['response']['players'][0]

        #obróbka obiektów
        count_of_games = steamgamesinfo['game_count']
        steamgamesinfo = steamgamesinfo['games']
        steamgamesinfo.sort(key=sortkey, reverse=True)
        usersummary = {"avatar": usersummary['avatarfull'],"personaname": usersummary['personaname'],'url':usersummary['profileurl']}
        zwrot = {"steam":usersummary}

        steamgamesinfokeys = dict.fromkeys(range(1, len(steamgamesinfo)))
        steamgamesinfo = dict(zip(steamgamesinfokeys,steamgamesinfo))
        print(type(steamgamesinfo))
        return zwrot

    

if __name__ == "__main__":
    app.run(debug=True)
