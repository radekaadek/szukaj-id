import requests
from ast import literal_eval
from base64 import b64decode

hypixel_url = 'https://api.hypixel.net'
hypixel_api_key = '36da01f0-28b9-4bc1-9c33-d24c57f55399'
mojang_url = 'https://api.mojang.com/users/profiles/minecraft/'
mojang_skin_url = 'https://sessionserver.mojang.com/session/minecraft/profile' #uuid

username = 'radekaadek'

# returns a dict of data from the api
def faster(route, uuid) -> dict:
    PARAMS = {'key': hypixel_api_key, 'uuid': uuid}
    faster_json = requests.get(hypixel_url + '/' + route, params=PARAMS)
    faster_data = faster_json.json()
    return faster_data

# rank, aliases last_seen values can be 'ZAMKOR' if not found,
# this depends on the age of a players account
def dane(username) -> dict:
    uuid = requests.get(f'{mojang_url}{username}').json()['id']
    #hypixel data
    player_status = faster('status', uuid)['session']['online']
    stats = faster('player', uuid)
    try:
        rank = stats['player']['rank']
    except:
        rank = 'ZAMKOR'
    # print(stats['player'])
    # for key, value in stats['player'].items() :
    #     print(f'{key} {value}')
    try:
        aliases = stats['player']['knownAliases']
    except:
        aliases = 'ZAMKOR'
    try:
        last_seen = stats['player']['lastLogout']
    except:
        last_seen = 'ZAMKOR'
    #skin
    mojang_data = requests.get(f'{mojang_skin_url}/{uuid}').json()
    decoded_string = b64decode(mojang_data['properties'][0]['value']).decode('utf-8')
    skin_url = literal_eval(decoded_string)['textures']['SKIN']['url']
    return {'status': player_status, 'last_seen': last_seen, 'aliases': aliases, 'rank': rank, 'skin_url': skin_url}


print(dane(username))
