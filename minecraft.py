from unicodedata import name
from xmlrpc.client import Boolean
import aiohttp, asyncio
from datetime import datetime, timedelta

hypixel_url = 'https://api.hypixel.net'
hypixel_api_key = '36da01f0-28b9-4bc1-9c33-d24c57f55399'
mojang_url = 'https://api.mojang.com/users/profiles/minecraft/'
mojang_skin_url = 'https://sessionserver.mojang.com/session/minecraft/profile' #/uuid

# head api: https://mc-heads.net
#mojang api docs: https://wiki.vg/Mojang_API
#hypixel api docs: https://api.hypixel.net/#tag/Player-Data/paths/~1player/get

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# rank, aliases last_seen values can be 'False' if not found,
# this depends on the age of a players account and hypixels data
async def dane(username, session) -> dict:
    # get uuid from mojang
    try:
        async with session.get(f'{mojang_url}{username}') as response:
            r1 = await response.json()
            uuid = r1['id']
    except:
        return {'error': 'NOT_FOUND'}
    #hypixel data
    route = 'status'
    name_data = {}
    PARAMS = {'key': hypixel_api_key, 'uuid': uuid}
    async with session.get(hypixel_url + '/' + route, params=PARAMS) as response:
        status_response = await response.json()
        player_status = status_response['session']['online']
    route2 = 'player'
    PARAMS = {'key': hypixel_api_key, 'uuid': uuid}
    async with session.get(hypixel_url + '/' + route2, params=PARAMS) as response:
        stats = await response.json()
    try:
        rank = stats['player']['rank']
    except:
        rank = False
    try:
        aliases = stats['player']['knownAliases']
        if len(aliases) > 1:
            name_data['aliases'] = aliases
        else:
            name_data['aliases'] = 0
    except:
        name_data['aliases'] = 0
    try:
        last_seen_milis = stats['player']['lastLogout']
        last_seen = (datetime(1970, 1, 1) + timedelta(milliseconds=last_seen_milis)).replace(microsecond=0)
    except:
        last_seen = False 
    if name_data['aliases'] == 0:
        name_data['name'] = username
    else:
        name_data['name'] = aliases[-1]
    player_data = name_data | {'last_seen': last_seen, 'rank': rank, 'profile_link': f'https://plancke.io/hypixel/player/stats/{username}', 'status': 'online' if player_status else 'offline'}
    return player_data | {'avatar': f'https://mc-heads.net/avatar/{username}/nohelm', 'error': 'OK'}
