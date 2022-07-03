A website that allows you to check someones ingame stats!

Running the server: 
Make sure to have a Python 3.10+ interpreter installed on your machine,
Enter the project directory in your operating systems terminal and run:

On powershell (windows):

1. pip install venv // install virtual enviroment
2. ./venv/scripts/activate  // activate
3. pip install requirements.txt  // install requirements
4. uvicorn main:app  // run server

On bash (linux/mac):

1. pip install venv // install virtual enviroment
2. source venv/bin/activate
3. pip install requirements.txt  // install requirements
4. uvicorn main:app

Build with Fast API
Every api request uses an aiohttp session
