# A website that allows you to check someones ingame stats!

No one likes to manualy check someones profiles on major platforms
to find out who they are, so we made a website for that
Open-source, without any annoying ads and tracking!

# Running the server: 

1. Make sure to have a Python 3.10+ interpreter installed on your machine,
2. Create an api_keys.py file in the same directory as this file with the following content:

    steam_api_key = ""
    riot_api_key = ""
    fortnite_api_key = ""
    hypixel_api_key = ""

    Now insert your api keys into the api_keys.py file.

    Your can get them from:
        https://steamcommunity.com/dev/apikey
        https://developer.riotgames.com
        https://dash.fortnite-api.com/account
        https://api.hypixel.net/#section/Authentication

3. Enter the project directory in your operating systems terminal and run:

On powershell (windows):

1. pip install venv // install virtual enviroment
2. ./venv/scripts/activate  // activate
3. pip install -r requirements.txt  // install requirements
4. uvicorn main:app --reload --port 80  // run server

On bash (linux/mac):

1. pip install venv // install virtual enviroment
2. source venv/bin/activate //activate
3. pip install -r requirements.txt // install requirements
4. uvicorn main:app --reload --port 80 // run server

For running the image_cropper.py script use pip install Pillow

Build with Fast API
Every api request uses an aiohttp session

