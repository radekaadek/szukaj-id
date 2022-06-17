from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio, aiohttp, uvicorn, steam
import fortnite as fn
import minecraft as mc
import league_of_legends_new as lol

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#regiony = ['Brasil', 'Europe Nordic & East', 'Europe West', 'Japan', 'Korea', 'Latin America North', 'Latin America South', 'North America', 'Oceania', 'Russia', 'Turkey']

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) #na linuxie usunac

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

@app.get('/{username}', response_class=HTMLResponse)
async def search(username, request: Request):
    #nazwa z formularza
    async with aiohttp.ClientSession() as session:
        fortnite_task = asyncio.create_task(fn.dane(username, session))
        minecraftTask = asyncio.create_task(mc.dane(username, session))
        steamTask = asyncio.create_task(steam.checkSteam(username, session))
        lolTask = asyncio.create_task(lol.dane(username, session))
        zwrot = {'fortnite': "await fortnite_task", 'lol': "await lolTask", 'minecraft': await minecraftTask, 'steam': await steamTask}
    return templates.TemplateResponse("new_home.html", {'request': request, 'zwrot': zwrot})
    
if __name__ == "__main__":
    uvicorn.run(app, port=8000)
