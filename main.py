from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio, aiohttp, uvicorn, steam
import fortnite as fn
import minecraft as mc
import league_of_legends_new as lol
import snapchat as snap

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#regions = ['Brasil', 'Europe Nordic & East', 'Europe West', 'Japan', 'Korea', 'Latin America North', 'Latin America South', 'North America', 'Oceania', 'Russia', 'Turkey']

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # delete on linux

@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {'request': request})

@app.get('/{username}', response_class=HTMLResponse)
async def search(username, request: Request) -> HTMLResponse:
    # easter egg
    if username == "agroursusowo":
        return templates.TemplateResponse("pit.html", {'request': request})
    async with aiohttp.ClientSession() as session:
        fortnite_task = asyncio.create_task(fn.dane(username, session))
        minecraft_task = asyncio.create_task(mc.dane(username, session))
        steam_task = asyncio.create_task(steam.check_steam(username, session))
        lol_task = asyncio.create_task(lol.data(username, session))
        snap_task = asyncio.create_task(snap.data(username, session))
        zwrot = {'fortnite': await fortnite_task, 'lol': await lol_task, 'minecraft': await minecraft_task, 'steam': await steam_task, 'snap': await snap_task}
        # print(zwrot)   #debug
    return templates.TemplateResponse("new_home.html", {'request': request, 'zwrot': zwrot})
    
if __name__ == "__main__":
    uvicorn.run(app, port=80)
