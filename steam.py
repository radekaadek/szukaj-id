from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
import operator
sortkey= operator.itemgetter('playtime_forever')

def arrayToDictionary(arrlist):
    arrlistkeys = dict.fromkeys(range(1, len(arrlist)))
    arrlist = dict(zip(arrlistkeys,arrlist))
    return arrlist

def checkSteam(nazwa_uzytkownika,steam_api_key):
    #dokumentacja: https://pypi.org/project/steamwebapi/
    #deklaracje głównych interfejsów API steam
    steamuserinfo = ISteamUser(steam_api_key = steam_api_key) 
    steamplayerinfo = IPlayerService(steam_api_key = steam_api_key)
    steamstatsinfo = ISteamUserStats(steam_api_key = steam_api_key)
    
    try:
        #api request by pozyskać steam ID
        steamid = steamuserinfo.resolve_vanity_url(str(nazwa_uzytkownika), format="json")['response']['steamid']

        #api request by pozyskać dane w obiektach
        steamgamesinfo = steamplayerinfo.get_owned_games(steamid, format="json")['response']
        usersummary = steamuserinfo.get_player_summaries(steamid, format="json")['response']['players'][0]
        levelsteam = steamplayerinfo.get_steam_level(steamid, format="json")['response']
        #obróbka obiektów
        count_of_games = steamgamesinfo['game_count']
        steamgamesinfo = steamgamesinfo['games']
        steamgamesinfo.sort(key=sortkey, reverse=True)

        usersummary = {"avatar": usersummary['avatarfull'],"personaname": usersummary['personaname'],'url':usersummary['profileurl'],"favgames":arrayToDictionary(steamgamesinfo[0:4]),"gamequantity":count_of_games,"level":levelsteam['player_level']}
        return usersummary
    except:   return None