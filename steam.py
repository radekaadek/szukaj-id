from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
import operator

sortkey = operator.itemgetter("playtime_forever")


def arrayToDictionary(arrlist):
    arrlistkeys = dict.fromkeys(range(1, len(arrlist)))
    arrlist = dict(zip(arrlistkeys, arrlist))
    return arrlist


async def checkSteam(nazwa_uzytkownika, steam_api_key):
    # dokumentacja: https://pypi.org/project/steamwebapi/
    # deklaracje głównych interfejsów API steam
    try:
        steamuserinfo = ISteamUser(steam_api_key=steam_api_key)
        steamplayerinfo = IPlayerService(steam_api_key=steam_api_key)
        steamstatsinfo = ISteamUserStats(steam_api_key=steam_api_key)
    except:
        return {'error': 'API_KEY_ERROR'}

    try:
        # api request by pozyskać steam ID
        steamid = steamuserinfo.resolve_vanity_url(str(nazwa_uzytkownika), format="json")["response"]["steamid"]
    except:
        return {'error': 'USERNAME_ERROR'}
    try:
        # api request by pozyskać dane w obiektach
        steamgamesinfo = steamplayerinfo.get_owned_games(steamid, format="json")["response"]
        usersummary = steamuserinfo.get_player_summaries(steamid, format="json")["response"]["players"][0]
        levelsteam = steamplayerinfo.get_steam_level(steamid, format="json")["response"]

        # obróbka obiektów
        count_of_games = steamgamesinfo["game_count"]
        steamgamesinfo = steamgamesinfo["games"]
        steamgamesinfo.sort(key=sortkey, reverse=True)

        match usersummary['personastate']:
            case 0:
                status = 0
            case 1:
                status = 1
            case 2:
                status = 2
            case 3:
                status = 2
            case 4:
                status = 2
            case 5:
                status = 1
            case 6:
                status = 1

        usersummary = {
            "avatar": usersummary["avatarfull"],
            "personaname": usersummary["personaname"],
            "url": usersummary["profileurl"],
            "favgames": arrayToDictionary(steamgamesinfo[0:4]),
            "gamequantity": count_of_games,
            "status": status,
            "level": levelsteam["player_level"],
        }
        return usersummary
    except:
        return {'error': 'USERNAME_ERROR'}
