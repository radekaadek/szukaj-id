import aiohttp
import asyncio

fortnite_api_key = 'b4dab92b-ac98-4d0f-8cc9-5e2bc93de384'
fortnite_api_website = 'https://fortnite-api.com/v2/stats/br/v2'

#dokumentacja: https://dash.fortnite-api.com/endpoints/stats
#['image_url', 'raw_data', 'stats', 'user']
#[26:]
#.raw_data['all']['overall']['kd']
#'ninja' - niepubliczny

async def dane(username, session, platform='epic') -> dict:
    params = {'accountType': platform, 'name': username}
    headers = {'Authorization': fortnite_api_key}
    async with session.get(fortnite_api_website, params=params, headers=headers) as response:
        json_response = await response.json()
        if json_response['status'] == 403:
            # players account stats are private
            return {'error': 'PRIVATE'}
        if json_response['status'] == 404:
            # player not found
            return {'error': 'NOT_FOUND'}
        name = json_response['data']['account']['name']
        game_data = json_response['data']['stats']['all']['overall']     
        minutesPlayed = game_data['minutesPlayed']
        wins = game_data['wins']
        lastPlayed = game_data['lastModified']
    return {'error': 'OK', 'name': name, 'minutesPlayed': minutesPlayed, 'wins': wins, 'lastPlayed': lastPlayed}
    
