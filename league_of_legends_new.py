import aiohttp, asyncio
from datetime import datetime, timedelta
from api_keys import riot_api_key
if riot_api_key == "":
    print("Please set your riot api key in api_keys.py")

# documentation: https://riot-watcher.readthedocs.io/en/latest/index.html
# https://developer.riotgames.com/apis

regiony = {'Brasil': 'br1', 'Europe Nordic & East': 'eun1', 'Europe West': 'euw1', 'Japan': 'jp1', 'Korea': 'kr', 'Latin America North': 'la1', 'Latin America South': 'la2', 'North America': 'na1', 'Oceania': 'oc1', 'Russia': 'ru', 'Turkey': 'tr1'}

def return_region(nazwa_regionu) -> str:
    return regiony[nazwa_regionu]

def profile_link(username, region) -> dict:
    regiony_opgg = {'Brasil': 'br', 'Europe Nordic & East': 'eune', 'Europe West': 'euw', 'Japan': 'jp', 'Korea': 'kr', 'Latin America North': 'lan', 'Latin America South': 'las', 'North America': 'na', 'Oceania': 'oc', 'Russia': 'ru', 'Turkey': 'tr'}
    return {'link':f'https://{regiony_opgg[region]}.op.gg/summoner/userName={username}'}

async def data(summonerName, session, region='Europe Nordic & East') -> dict:
    base_region = return_region(region)
    base_url = f'https://{base_region}.api.riotgames.com'
    base_params = {"api_key": riot_api_key}
    async with session.get('https://ddragon.leagueoflegends.com/api/versions.json') as lvr:
        lv = await lvr.json()
        league_version = lv[0]
    async with session.get(f'{base_url}/lol/summoner/v4/summoners/by-name/{summonerName}', params=base_params) as response:
        if response.status == 200:
            return_dict = {'error': 'OK'}
            player_response = await response.json()
            # puuid = player_response['puuid'] # might be useful later
            level = player_response['summonerLevel']
            return_dict['level'] = level
            return_dict['revisionDate'] = (datetime(1970, 1, 1) + timedelta(milliseconds=player_response['revisionDate'])).replace(microsecond=0)
            return_dict['name'] = player_response['name']
            encryptedSummonerId = player_response['id']
            profileIconLink = f'https://ddragon.leagueoflegends.com/cdn/{league_version}/img/profileicon/{player_response["profileIconId"]}.png'
            return_dict['avatar'] = profileIconLink
            element = {}
            async with session.get(f'{base_url}/lol/league/v4/entries/by-summoner/{encryptedSummonerId}', params = base_params) as ranked_response:
                ranked_json_response = await ranked_response.json()
                for element in ranked_json_response:
                    if element['queueType'] == 'RANKED_SOLO_5x5':
                        if element['inactive'] == 'True':
                            return_dict['tier'] = 'inactive'
                            break
                        else:
                            return_dict['tier'] = element['tier'].lower().capitalize()
                            return_dict['rank'] = element['rank']
                            return_dict['leaguePoints'] = element['leaguePoints']
                            break
                if 'queueType' not in element:
                    return_dict['tier'] = 'inactive'
                return_dict |= profile_link(summonerName, region)
                print('lol done!')
                return return_dict
        elif response.status == 404:
            return {'error': 'NOT_FOUND'}
        elif response.status == 401 or response.status == 429:
            return {'error': 'API_ERROR'}
        elif response.status == 403:
            return {'error': 'KEY_ERROR'}
