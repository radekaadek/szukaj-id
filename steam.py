import aiohttp, asyncio, operator

sortkey = operator.itemgetter("playtime_forever")

steam_api_key = 'EE03692ACB03E4371522180E26926643'

def arrayToDictionary(arrlist):
    arrlistkeys = dict.fromkeys(range(1, len(arrlist)))
    arrlist = dict(zip(arrlistkeys, arrlist))
    keys_values = arrlist.items()
    arrlist = {str(key): value for key, value in keys_values}
    return arrlist


async def checkSteam(username, session):
    # dokumentacja: https://pypi.org/project/steamwebapi/
    # deklaracje głównych interfejsów API steam
    try:
        # api request by pozyskać steam ID
        params = {'vanityurl': username, 'key': steam_api_key}
        async with session.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/', params=params) as resp:
            data = await resp.json()
            if data['response']['success'] == 42:
                return {'error': 'NOT_FOUND'}
            steamid = data['response']['steamid']
    except:
        return {'error': 'API_ERROR'}
    # try:
    # api request by pozyskać dane w obiektach
    ##definicje: https://github.com/shawnsilva/steamwebapi/blob/devel/steamwebapi/api.py
    params = {'steamid': steamid, 'key': steam_api_key, 'include_appinfo': 1}
    async with session.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v1', params=params) as resp:
        steamgamesinfo_response = await resp.json()
        steamgamesinfo = steamgamesinfo_response["response"]

    params2 = {'steamids': steamid, 'key': steam_api_key}
    async with session.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params=params2) as resp:
        steamgamesinfo_response = await resp.json()
        usersummary = steamgamesinfo_response["response"]["players"][0]

    params3 = {'steamid': steamid, 'key': steam_api_key}
    async with session.get('http://api.steampowered.com/IPlayerService/GetSteamLevel/v1', params=params3) as resp:
        steamgamesinfo_response = await resp.json()
        levelsteam = steamgamesinfo_response["response"]

    # obróbka obiektów
    steamgamesinfo = steamgamesinfo["games"]
    steamgamesinfo.sort(key=sortkey, reverse=True)
    steamgamesinfo = steamgamesinfo[0:4]
    steamgamesinfo = arrayToDictionary(steamgamesinfo)
    
    for a in steamgamesinfo:
        del a["playtime_windows_forever"]
        del a["playtime_mac_forever"]
        del a["playtime_linux_forever"]
        a['icon_link'] = 'http://media.steampowered.com/steamcommunity/public/images/apps/' + str(a['appid']) + '/' + str(a['img_icon_url'])
        del a["img_icon_url"]
        del a["appid"]

    print(steamgamesinfo)

    match usersummary['personastate']:
        case 0:
            status = 'offline'
        case 1 | 5 | 6:
            status = 'online'
        case 2 | 3 | 4:
            status = 'busy'

    usersummary = {
        "avatar": usersummary["avatarfull"],
        "personaname": usersummary["personaname"],
        "url": usersummary["profileurl"],
        "favgames": steamgamesinfo,
        "status": status,
        "level": levelsteam["player_level"],
    }
    return usersummary | {'error': 'OK'}
    # except:
        # return {'error': 'NOT_FOUND'}
