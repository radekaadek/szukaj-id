from flask import Flask, render_template, request, redirect
import league_of_legends as lol
import steam, asyncio
import fortnite as fn
import hypixel_sync_copy as hyp

#regiony = ['Brasil', 'Europe Nordic & East', 'Europe West', 'Japan', 'Korea', 'Latin America North', 'Latin America South', 'North America', 'Oceania', 'Russia', 'Turkey']

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) #na linuxie usunac

app = Flask(__name__)
steam_api_key = 'EE03692ACB03E4371522180E26926643'

@app.route("/")
def index():
    return render_template("new_home.html")

@app.route('/<username>', methods = ['GET'])
async def search(username):
    #nazwa z formularza
    fortnite_task = asyncio.create_task(fn.dane(username))
    minecraftTask = asyncio.create_task(hyp.dane(username))
    steamTask = asyncio.create_task(steam.checkSteam(username, steam_api_key))
    region_gracza = lol.zwroc_region('Europe Nordic & East')
    graczLOL = lol.player(username, region_gracza)
    match graczLOL.czy_istnieje():
            case True : 
                zwrotLol = {
                            'error': 'OK',
                            "avatar": graczLOL.avatar(),
                            "personaname": graczLOL.link_do_profilu()['name1'],
                            'url':graczLOL.link_do_profilu()['link'],
                            "level":graczLOL.poziom(),
                            "wins":graczLOL.wins(),
                            "losses":graczLOL.losses(),
                            "tier":graczLOL.tier(),
                            "isLOL": True,
                            "rank":graczLOL.rank(),
                            "lp":graczLOL.league_points(),
                            }
            case False : zwrotLol = None
            case _: {'error': 'BRAK_GRACZA'}

    zwrot = {"steam":await steamTask, "lol":zwrotLol, 'minecraft': await minecraftTask, 'fortnite': await fortnite_task}
    return render_template("new_home.html", zwrot=zwrot) 
    
if __name__ == "__main__":
    app.run(debug=True)