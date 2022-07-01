import aiohttp, asyncio
from datetime import datetime, timedelta

hypixel_url = 'https://api.hypixel.net'
hypixel_api_key = '36da01f0-28b9-4bc1-9c33-d24c57f55399'
mojang_url = 'https://api.mojang.com/users/profiles/minecraft/'
mojang_skin_url = 'https://sessionserver.mojang.com/session/minecraft/profile' #/uuid

# api do glowy: https://mc-heads.net
#mojang api docs: https://wiki.vg/Mojang_API
#hypixel api docs: https://api.hypixel.net/#tag/Player-Data/paths/~1player/get

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# rank, aliases last_seen values can be 'False' if not found,
# this depends on the age of a players account
# if the skin is default, it will return 'default': True, in this case the skin has a diffrent size
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
    except:
        aliases = ["gsrukgf@#$uygau68465khsgf"]
    try:
        last_seen_milis = stats['player']['lastLogout']
        last_seen = (datetime(1970, 1, 1) + timedelta(milliseconds=last_seen_milis)).replace(microsecond=0)
    except:
        last_seen = False
    player_data = {'last_seen': last_seen, 'name': username, 'rank': rank, 'profile_link': f'https://plancke.io/hypixel/player/stats/{username}', 'status': 'online' if player_status else 'offline'}
    return player_data | {'avatar': f'https://mc-heads.net/avatar/{username}/nohelm', 'error': 'OK', 'aliases': ', '.join(aliases)}
