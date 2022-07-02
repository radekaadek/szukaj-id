A website that allows you to check someones ingame stats!

Running the server: 
Make sure to have python 3.10+ interpreter installed on your mashine,
Enter the project directory in your operating systems terminal and run:

On powershell (windows):

1. pip install requirements.txt  // install requirements
2. ./venv/scripts/activate  // activate virtual environment
3. uvicorn main:app  // run server

On bash (linux/mac):

1. source venv/bin/activate
2. uvicorn main:app

Build with Fast API
Every api request uses an aiohttp session
