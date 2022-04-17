from flask import Flask, render_template, request
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
from steamwebapi import profiles

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods = ["POST", "GET"])
def search():
    nazwa_uzytkownika = request.form["nazwa_uzytkownika"]

    steam_api_key = 'EE03692ACB03E4371522180E26926643'
    steamuserinfo = ISteamUser(steam_api_key=steam_api_key)
    steamid = steamuserinfo.resolve_vanity_url(str(nazwa_uzytkownika), format="json")['response']['steamid']
    usersummary = steamuserinfo.get_player_summaries(steamid, format="json")['response']['players'][0]

    return usersummary

if __name__ == "__main__":
    app.run(debug=True)
