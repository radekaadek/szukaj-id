import aiohttp
import asyncio

hypixel_url = 'https://api.hypixel.net'
hypixel_api_key = '36da01f0-28b9-4bc1-9c33-d24c57f55399'
mojang_url = 'https://api.mojang.com/users/profiles/minecraft/'
mojang_skin_url = 'https://sessionserver.mojang.com/session/minecraft/profile' #/uuid

# api do glowy: https://mc-heads.net
#mojang api docs: https://wiki.vg/Mojang_API
#hypixel api docs: https://api.hypixel.net/#tag/Player-Data/paths/~1player/get

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# returns a dict of data from hypixels api
async def request_pipeline(session, route, uuid) -> dict:
    PARAMS = {'key': hypixel_api_key, 'uuid': uuid}
    async with session.get(hypixel_url + '/' + route, params=PARAMS) as response:
        return await response.json()

async def hypixel_data(session, uuid) -> dict:
    status_response = await request_pipeline(session, 'status', uuid)
    stats = await request_pipeline(session, 'player', uuid)
    player_status = status_response['session']['online']
    try:
        rank = stats['player']['rank']
    except:
        rank = False
    try:
        aliases = stats['player']['knownAliases']
    except:
        aliases = False
    try:
        last_seen = stats['player']['lastLogout']
    except:
        last_seen = False
    return {'online_status': player_status, 'last_seen': last_seen, 'aliases': aliases, 'rank': rank}

# rank, aliases last_seen values can be 'False' if not found,
# this depends on the age of a players account
# if the skin is default, it will return 'default': True, in this case the skin has a diffrent size
async def dane(username, session) -> dict:
    try:
        async with session.get(f'{mojang_url}{username}') as response:
            r1 = await response.json()
            uuid = r1['id']
    except:
        return {'error': 'NOT_FOUND'}
#hypixel data
    player_data = await hypixel_data(session, uuid)
    return player_data | {'skin_url': f'https://mc-heads.net/avatar/{username}'}
