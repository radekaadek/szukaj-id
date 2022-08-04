import operator
from api_keys import steam_api_key
if steam_api_key == "":
    print("Please set your steam api key in api_keys.py")

sortkey = operator.itemgetter("playtime_forever")

def arrayToDictionary(arrlist) -> dict:
    arrlistkeys = dict.fromkeys(range(1, len(arrlist)))
    arrlist = dict(zip(arrlistkeys, arrlist))
    keys_values = arrlist.items()
    arrlist = {str(key): value for key, value in keys_values}
    return arrlist

def get_name(usersummary):
    return usersummary['personaname']


async def checkSteam(username, session, steamid='') -> dict:
    # documentation: https://wiki.teamfortress.com/wiki/WebAPI
    try:
        # api request to get steam ID
        params = {'vanityurl': username, 'key': steam_api_key}
        async with session.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/', params=params) as resp:
            data = await resp.json()
            if data['response']['success'] == 42:
                return {'error': 'NOT_FOUND'}
            steamid = data['response']['steamid']
    except:
        return {'error': 'NOT_FOUND'}
    # api request by pozyskać dane w obiektach
    ##definicje: https://github.com/shawnsilva/steamwebapi/blob/devel/steamwebapi/api.py
    params = {'steamid': steamid, 'key': steam_api_key, 'include_appinfo': 1}
    async with session.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v1', params=params) as resp:
        steamgamesinfo_response = await resp.json()
        steamgamesinfo = steamgamesinfo_response["response"]

    # get players level
    params3 = {'steamid': f'{steamid}', 'key': steam_api_key}
    async with session.get('http://api.steampowered.com/IPlayerService/GetSteamLevel/v1', params=params3) as resp:
        steamgamesinfo_response = await resp.json()
        levelsteam = steamgamesinfo_response["response"]

    friend_dict = {}
    friend_ids = ''
    # friends
    params = {'steamid': steamid, 'key': steam_api_key, 'relationship': 'friend'}
    async with session.get('http://api.steampowered.com/ISteamUser/GetFriendList/v1', params=params) as resp:
        steamfriends_response = await resp.json()
        if steamfriends_response == {}:
            friend_dict['number_of_friends'] = 0
        else:    
            friend_dict['number_of_friends'] = len(steamfriends_response['friendslist']['friends'])
            for friend in steamfriends_response['friendslist']['friends']:
                friend_ids += f',{friend["steamid"]}'

    params2 = {'steamids': f'{steamid}{friend_ids}', 'key': steam_api_key}
    async with session.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params=params2) as resp:
        steamgamesinfo_response = await resp.json()
        # find target player in summaries
        if friend_dict['number_of_friends'] != 0:
            for player in steamgamesinfo_response['response']['players']:
                if str(player['steamid']) == steamid:
                    usersummary = player
                    friend_dict['friends'] = steamgamesinfo_response['response']['players']
                    friend_dict['friends'].remove(player)
                    friend_dict['friends'].sort(key=get_name)
                    break
        else:
            usersummary = steamgamesinfo_response['response']['players'][0]
            friend_dict['friends'] = []
        
        # obróbka obiektów
        try:
            steamgamesinfo = steamgamesinfo["games"]
        except:
            return {'error': 'NOT_FOUND'}
        steamgamesinfo.sort(key=sortkey, reverse=True)
        steamgamesinfo = steamgamesinfo[0:4]
        steamgamesinfo = arrayToDictionary(steamgamesinfo)
        
        for a in steamgamesinfo:
            del steamgamesinfo[a]["playtime_windows_forever"]
            del steamgamesinfo[a]["playtime_mac_forever"]
            del steamgamesinfo[a]["playtime_linux_forever"]
            steamgamesinfo[a]['icon_link'] = f'http://media.steampowered.com/steamcommunity/public/images/apps/{steamgamesinfo[a]["appid"]}/{steamgamesinfo[a]["img_icon_url"]}.jpg'
            del steamgamesinfo[a]["img_icon_url"]
            del steamgamesinfo[a]["appid"]
    

    if usersummary['personastate'] == 0:
        status = 'offline'
    elif usersummary['personastate'] == 1 or usersummary['personastate'] == 5 or usersummary['personastate'] == 6:
        status = 'online'
    elif usersummary['personastate'] == 2 or usersummary['personastate'] == 3 or usersummary['personastate'] == 4:
        status = 'busy' 


    usersummary = {
        "avatar": usersummary["avatarfull"],
        "personaname": usersummary["personaname"],
        "url": usersummary["profileurl"],
        "favgames": steamgamesinfo,
        "status": status,
        "level": levelsteam["player_level"]
    }
    print('steam done!')
    return friend_dict | usersummary | {'error': 'OK'}
