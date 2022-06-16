from flask import Flask, render_template, request, redirect
import steam, asyncio, aiohttp, time
import league_of_legends as lol
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
    start = time.time()
    async with aiohttp.ClientSession() as session:
        fortnite_task = asyncio.create_task(fn.dane(username, session))
        start2 = time.time()
        minecraftTask = asyncio.create_task(hyp.dane(username, session))
        steamTask = asyncio.create_task(steam.checkSteam(username, steam_api_key, session))
        start3 = time.time()
        zwrot = {"steam": await steamTask, 'minecraft': await minecraftTask, 'fortnite': await fortnite_task}
    end = time.time()
    zwrot = zwrot | {'time': end - start, 'time2': end - start2, 'time3': end - start3}
    return render_template("new_home.html", zwrot=zwrot) 
    
if __name__ == "__main__":
    app.run(debug=True)