from flask import Flask, render_template, request, redirect
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
from steamwebapi import profiles
import json, operator
import league_of_legends as lol

#regiony = ['Brasil', 'Europe Nordic & East', 'Europe West', 'Japan', 'Korea', 'Latin America North', 'Latin America South', 'North America', 'Oceania', 'Russia', 'Turkey']

app = Flask(__name__)
sortkey= operator.itemgetter('playtime_forever')
steam_api_key = 'EE03692ACB03E4371522180E26926643'

region_gracza = lol.zwroc_region('Europe Nordic & East')
nazwa_gracza = 'wiesiek5monster'

gracz = lol.player(nazwa_gracza, region_gracza)
zwrotDanych = {}
print(gracz.avatar())

def arrayToDictionary(arrlist):
    arrlistkeys = dict.fromkeys(range(1, len(arrlist)))
    arrlist = dict(zip(arrlistkeys,arrlist))
    return arrlist

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
    
    try:
        #api request by pozyskać steam ID
        steamid = steamuserinfo.resolve_vanity_url(str(nazwa_uzytkownika), format="json")['response']['steamid']

        #api request by pozyskać dane w obiektach
        steamgamesinfo = steamplayerinfo.get_owned_games(steamid, format="json")['response']
        usersummary = steamuserinfo.get_player_summaries(steamid, format="json")['response']['players'][0]

        #obróbka obiektów
        count_of_games = steamgamesinfo['game_count']
        steamgamesinfo = steamgamesinfo['games']
        steamgamesinfo.sort(key=sortkey, reverse=True)

        usersummary = {"avatar": usersummary['avatarfull'],"personaname": usersummary['personaname'],'url':usersummary['profileurl'],"favgames":arrayToDictionary(steamgamesinfo[0:4]),"gamequantity":count_of_games}
        zwrot = {"steam":usersummary}


        return zwrot
    except:   return "ZAMKOR"
    

if __name__ == "__main__":
    app.run(debug=True)
