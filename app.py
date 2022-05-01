from ast import match_case
from flask import Flask, render_template, request, redirect
import league_of_legends as lol
import steam, asyncio

#regiony = ['Brasil', 'Europe Nordic & East', 'Europe West', 'Japan', 'Korea', 'Latin America North', 'Latin America South', 'North America', 'Oceania', 'Russia', 'Turkey']

app = Flask(__name__)
steam_api_key = 'EE03692ACB03E4371522180E26926643'

def czy_wszystko_none(dane):
    for i in dane:
        if dane[i] != None:
            return False
    return True


def czy_wszystko_none(dane):
    for i in dane:
        if dane[i] != None:
            return False
    return True

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/search", methods = ["POST", "GET"])
async def search():
    #nazwa z formularza
    nazwa_uzytkownika = request.form["nazwa_uzytkownika"] 

    region_gracza = lol.zwroc_region('North America')
    graczLOL = lol.player(nazwa_uzytkownika, region_gracza)

    steamTask = asyncio.create_task(steam.checkSteam(nazwa_uzytkownika, steam_api_key))
    graczLOL.czy_w_grze()
    graczLOL.ranga()
    
    
    
    
    match graczLOL.czy_istnieje():
            case True : zwrotLol = {"avatar": graczLOL.avatar(),"personaname": graczLOL.link_do_profilu()['name1'],'url':graczLOL.link_do_profilu()['link'],"level":graczLOL.poziom(), "wins":graczLOL.ranga()[3],"losses":graczLOL.ranga()[4],"tier":graczLOL.ranga()[0],"rank":graczLOL.ranga()[1],"lp":graczLOL.ranga()[2]}
            case False : zwrotLol = None
            case _: print("Za dużo zapytań")

    zwrot = {"steam":await steamTask, "lol":zwrotLol} 
    
    if czy_wszystko_none(zwrot):
        return 'ZAMKOR'
    else: return zwrot

@app.route('/<piotr>', methods = ['GET', 'POST'])
def strona(piotr):
    return render_template("error.html", mordula = piotr)   
    
if __name__ == "__main__":
    app.run(debug=True)
