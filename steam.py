from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
import operator

sortkey = operator.itemgetter("playtime_forever")

def arrayToDictionary(arrlist):
    arrlistkeys = dict.fromkeys(range(1, len(arrlist)))
    arrlist = dict(zip(arrlistkeys, arrlist))
    return arrlist


async def checkSteam(username, steam_api_key, session):
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
    try:
        # api request by pozyskać dane w obiektach
        params = {'steamid': steamid, 'key': steam_api_key}
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
        count_of_games = steamgamesinfo["game_count"]
        steamgamesinfo = steamgamesinfo["games"]
        steamgamesinfo.sort(key=sortkey, reverse=True)

        match usersummary['personastate']:
            case 0:
                status = 0
            case 1 | 5 | 6:
                status = 1
            case 2 | 3 | 4:
                status = 2

        usersummary = {
            "avatar": usersummary["avatarfull"],
            "personaname": usersummary["personaname"],
            "url": usersummary["profileurl"],
            "favgames": arrayToDictionary(steamgamesinfo[0:4]),
            "gamequantity": count_of_games,
            "status": status,
            "level": levelsteam["player_level"],
        }
        return usersummary | {'error': 'OK'}
    except:
        return {'error': 'NOT_FOUND'}
