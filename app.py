from flask import Flask, render_template, request, redirect
import json, operator
import league_of_legends as lol
import steam

#regiony = ['Brasil', 'Europe Nordic & East', 'Europe West', 'Japan', 'Korea', 'Latin America North', 'Latin America South', 'North America', 'Oceania', 'Russia', 'Turkey']

app = Flask(__name__)
steam_api_key = 'EE03692ACB03E4371522180E26926643'

region_gracza = lol.zwroc_region('North America')
nazwa_gracza = 'mansplain'

gracz = lol.player(nazwa_gracza, region_gracza)
zwrotDanych = {}
print(gracz.czy_w_grze())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods = ["POST", "GET"])
def search():
    #nazwa z formularza
    nazwa_uzytkownika = request.form["nazwa_uzytkownika"]

    zwrot = {"steam":steam.checkSteam(nazwa_uzytkownika, steam_api_key)} 

    if len(zwrot) > 0:
        return zwrot

    
    

if __name__ == "__main__":
    app.run(debug=True)
