from flask import Flask, render_template, request
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
from steamwebapi import profiles
import json

app = Flask(__name__)

steam_api_key = 'EE03692ACB03E4371522180E26926643'
riot_api_key = 'RGAPI-872636ab-9da1-4355-8afa-a1ab624dd6f4'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods = ["POST", "GET"])
def search():
    #dokumentacja: https://pypi.org/project/steamwebapi/
    nazwa_uzytkownika = request.form["nazwa_uzytkownika"]

    steamuserinfo = ISteamUser(steam_api_key = steam_api_key)
    steamplayerinfo = IPlayerService(steam_api_key = steam_api_key, format="json")
    steamid = steamuserinfo.resolve_vanity_url(str(nazwa_uzytkownika), format="json")['response']['steamid']

    usersummary = steamuserinfo.get_player_summaries(steamid, format="json")['response']['players'][0]
    usersummary = {"avatar": usersummary['avatarfull'],"personaname": usersummary['personaname'],'url':usersummary['profileurl']}

    steamgamesinfo = steamplayerinfo.get_owned_games(steamid)

    

    zwrot = {"steam":usersummary}
    return steamgamesinfo

    

if __name__ == "__main__":
    app.run(debug=True)
