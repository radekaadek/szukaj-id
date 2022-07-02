A website that allows you to check someones ingame stats!

Running the server: enter the project directory in your operating systems terminal and run

On powershell (windows):

1. ./venv/scripts/activate
2. uvicorn main:app

On bash (linux/mac):

1. source venv/bin/activate
2. uvicorn main:app

Build with Fast API
Every api request uses an aiohttp session
