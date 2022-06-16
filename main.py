from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio, aiohttp, uvicorn, time, steam
import fortnite as fn
import minecraft as hyp

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#regiony = ['Brasil', 'Europe Nordic & East', 'Europe West', 'Japan', 'Korea', 'Latin America North', 'Latin America South', 'North America', 'Oceania', 'Russia', 'Turkey']

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) #na linuxie usunac

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("new_home.html", {'request': request})

@app.get('/{username}', response_class=HTMLResponse)
async def search(username, request: Request):
    #nazwa z formularza
    start = time.time()
    async with aiohttp.ClientSession() as session:
        fortnite_task = asyncio.create_task(fn.dane(username, session))
        minecraftTask = asyncio.create_task(hyp.dane(username, session))
        steamTask = asyncio.create_task(steam.checkSteam(username, session))
        zwrot = {"steam": await steamTask, 'minecraft': await minecraftTask, 'fortnite': await fortnite_task}
    end = time.time()
    zwrot = {'essa': zwrot} | {'time': end - start}
    return templates.TemplateResponse("new_home.html", zwrot | {'request': request}) 
    
if __name__ == "__main__":
    uvicorn.run(app)