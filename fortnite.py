import aiohttp
import asyncio

fortnite_api_key = ''
fortnite_api_website = 'https://fortnite-api.com/v2/stats/br/v2'

#dokumentacja: https://dash.fortnite-api.com/endpoints/stats
#['image_url', 'raw_data', 'stats', 'user']
#[26:]
#.raw_data['all']['overall']['kd']
#'ninja' - niepubliczny

username = 'radekaadek'

async def dane(username, platform='epic') -> dict:
    async with aiohttp.ClientSession() as session:
        params = {'accountType': platform, 'name': username}
        headers = {'Authorization': fortnite_api_key}
        async with session.get(fortnite_api_website, params=params, headers=headers) as response:
            json_response = await response.json()
            if json_response['status'] == 403:
                # players account stats are private
                return {'error': 'PRIVATE', 'name': 'ZAMKOR', 'raw_data': 'ZAMKOR'}
            if json_response['status'] == 404:
                # player not found
                return {'error': 'NOT_FOUND', 'name': 'ZAMKOR', 'raw_data': 'ZAMKOR'}
            name = json_response['data']['account']['name']
    return {'error': 'OK', 'name': name, 'raw_data': json_response['data']['account']}
    

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(dane(username))
