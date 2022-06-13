import requests
from ast import literal_eval
from base64 import b64decode

hypixel_url = 'https://api.hypixel.net'
hypixel_api_key = '36da01f0-28b9-4bc1-9c33-d24c57f55399'
mojang_url = 'https://api.mojang.com/users/profiles/minecraft/'
mojang_skin_url = 'https://sessionserver.mojang.com/session/minecraft/profile' #/uuid

username = 'radekaadek'

#mojang api docs: https://wiki.vg/Mojang_API
#hypixel api docs: https://api.hypixel.net/#tag/Player-Data/paths/~1player/get

# returns a players default skin name if they have one
# credit: https://github.com/crafatar/crafatar/blob/9d2fe0c45424de3ebc8e0b10f9446e7d5c3738b2/lib/skins.js#L90-L108
def default_skin(uuid) -> str:
    if (len(uuid)<= 16):
        return 'steve'
    lsbs_even = (
                    int(uuid[7], 16) ^
                    int(uuid[15], 16) ^
                    int(uuid[23], 16) ^
                    int(uuid[31], 16)
                )
    if lsbs_even:
        return 'alex'
    else:
        return 'steve'



# returns a dict of data from hypixels api
def request_pipeline(route, uuid) -> dict:
    PARAMS = {'key': hypixel_api_key, 'uuid': uuid}
    faster_json = requests.get(hypixel_url + '/' + route, params=PARAMS)
    faster_data = faster_json.json()
    return faster_data

def hypixel_data(uuid) -> dict:
    player_status = request_pipeline('status', uuid)['session']['online']
    stats = request_pipeline('player', uuid)
    try:
        rank = stats['player']['rank']
    except:
        rank = 'ZAMKOR'
    try:
        aliases = stats['player']['knownAliases']
    except:
        aliases = 'ZAMKOR'
    try:
        last_seen = stats['player']['lastLogout']
    except:
        last_seen = 'ZAMKOR'
    return {'online_status': player_status, 'last_seen': last_seen, 'aliases': aliases, 'rank': rank}

def mojang_data(uuid) -> dict:
    mojang_data = requests.get(f'{mojang_skin_url}/{uuid}').json()
    decoded_string = b64decode(mojang_data['properties'][0]['value']).decode('utf-8')
    default_skin = False
    try:
        skin_url = literal_eval(decoded_string)['textures']['SKIN']['url']
    except:
        default_skin = True
        if default_skin(uuid) == 'alex':
            skin_url = 'https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/4b/Alex_%28texture%29_JE1_BE1.png/revision/latest?cb=20201025200833'
        else:
            skin_url = 'https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d1/Steve_%28texture%29_JE4_BE2.png/revision/latest?cb=20210509095344'
    return {'default_skin': default_skin, 'skin_url': skin_url}

# rank, aliases last_seen values can be 'ZAMKOR' if not found,
# this depends on the age of a players account
# if the skin is default, it will return 'default': True, in this case the skin has a diffrent size
def dane(username) -> dict:
    uuid = requests.get(f'{mojang_url}{username}').json()['id']
    #hypixel data
    player_data = hypixel_data(uuid)
    #skin
    skin_data = mojang_data(uuid)
    return player_data | skin_data


print(dane(username))
