import requests

hypixel_url = 'https://api.hypixel.net'
hypixel_api_key = '36da01f0-28b9-4bc1-9c33-d24c57f55399'
mojang_url = 'https://api.mojang.com/users/profiles/minecraft/'

username = 'radekaadek'

# returns a dict of data from the api
def faster(route, uuid) -> dict:
    PARAMS = {'key': hypixel_api_key, 'uuid': uuid}
    faster_json = requests.get(hypixel_url + '/' + route, params=PARAMS)
    faster_data = faster_json.json()
    return faster_data



def dane(username) -> dict:
    uuid = requests.get(f'{mojang_url}{username}').json()['id']
    player_status = faster('status', uuid)['session']['online']
    stats = faster('player', uuid)
    print(stats['player'])
    for key, value in stats['player'].items() :
        print(f'{key} {value}')
    aliases = stats['player']['knownAliases']
    last_seen = stats['player']['lastLogout']
    return {'status': player_status, 'last_seen': last_seen, 'aliases': aliases}


print(dane(username))
