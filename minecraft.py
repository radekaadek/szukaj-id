from unicodedata import name
from xmlrpc.client import Boolean
import aiohttp, asyncio
from datetime import datetime, timedelta

hypixel_url = 'https://api.hypixel.net'
hypixel_api_key = '36da01f0-28b9-4bc1-9c33-d24c57f55399'
mojang_url = 'https://api.mojang.com/users/profiles/minecraft/'
mojang_skin_url = 'https://sessionserver.mojang.com/session/minecraft/profile' #/uuid

# head api: https://mc-heads.net
# mojang api docs: https://wiki.vg/Mojang_API
# hypixel api docs: https://api.hypixel.net/#tag/Player-Data/paths/~1player/get

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
    name_data = {}
    friends_list = []
    friend_uuids = []
    PARAMS = {'key': hypixel_api_key, 'uuid': uuid}
    async with session.get(hypixel_url + '/status', params=PARAMS) as response:
        status_response = await response.json()
        player_status = status_response['session']['online']

    async with session.get(hypixel_url + '/player', params=PARAMS) as response:
        stats = await response.json()
    async with session.get(hypixel_url + '/friends', params=PARAMS) as response:
        friends = await response.json()
    for friend in friends['records']:
        if friend['uuidSender'] != uuid:
            friend_uuids.append(friend['uuidSender'])
        else:
            friend_uuids.append(friend['uuidReceiver'])
    for friend_uuid in friend_uuids:
        async with session.get(hypixel_url + '/player', params={'key': hypixel_api_key, 'uuid': friend_uuid}) as response:
            friend_data = await response.json()
            if friend_data['success'] == True:
                friends_list.append( {'name': friend_data['player']['displayname'], 'avatar': f'https://mc-heads.net/avatar/{friend_data["player"]["displayname"]}/nohelm'})
    friends_list.sort(key=lambda x: x['name'])
    try:
        rank = stats['player']['rank']
    except:
        rank = False
    try:
        aliases = stats['player']['knownAliases']
        if len(aliases) > 1:
            name_data['aliases'] = aliases[:-1]
            name_data['name'] = aliases[-1]
        else:
            name_data['name'] = aliases[0]
            name_data['aliases'] = 0
    except:
        name_data['aliases'] = 0
        name_data['name'] = username
    try:
        last_seen_milis = stats['player']['lastLogout']
        last_seen = (datetime(1970, 1, 1) + timedelta(milliseconds=last_seen_milis)).replace(microsecond=0)
    except:
        last_seen = False 
    player_data = name_data | {'last_seen': last_seen, 'rank': rank, 'profile_link': f'https://plancke.io/hypixel/player/stats/{username}', 'status': 'online' if player_status else 'offline'}
    print('minecraft done!')
    return player_data | {'avatar': f'https://mc-heads.net/avatar/{username}/nohelm', 'error': 'OK'} | {'friends': friends_list, 'number_of_friends': len(friends_list)}
