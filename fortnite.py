import aiohttp
import asyncio
from api_keys import fortnite_api_key
if fortnite_api_key == "":
    print("Please set your fortnite api key in api_keys.py")

fortnite_api_website = 'https://fortnite-api.com/v2/stats/br/v2'

#dokumentacja: https://dash.fortnite-api.com/endpoints/stats

async def dane(username, session, platform='epic') -> dict:
    params = {'accountType': platform, 'name': username}
    headers = {'Authorization': fortnite_api_key}
    async with session.get(fortnite_api_website, params=params, headers=headers) as response:
        json_response = await response.json()
        if json_response['status'] == 403:
            # players account stats are private
            return {'error': 'PRIVATE'}
        elif json_response['status'] == 404:
            # player not found
            return {'error': 'NOT_FOUND'}
        elif json_response['status'] == 400 or json_response['status'] == 401:
            return {'error': 'API_ERROR'}
        name = json_response['data']['account']['name']
        bp_level = json_response['data']['battlePass']['level']
        game_data = json_response['data']['stats']['all']['overall']     
        hoursPlayed = game_data['minutesPlayed']//60
        wins = game_data['wins']
        lastPlayed = game_data['lastModified']
    if lastPlayed == '1970-01-01T00:00:00Z' or not hoursPlayed:
        return {'error': 'NOT_FOUND'}
    lastPlayed = lastPlayed.replace('T', ' ').replace('Z', '')
    print('fortnite done!')
    return {'error': 'OK', 'name': name, 'hoursPlayed': hoursPlayed, 'wins': wins, 'lastPlayed': lastPlayed, 'battlepassLevel': bp_level}
