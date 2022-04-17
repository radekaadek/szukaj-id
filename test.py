from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
from steamwebapi import profiles


def main():
    steam_api_key = 'EE03692ACB03E4371522180E26926643'

    plik = open('wynik.txt', 'w')
    steamuserinfo = ISteamUser(steam_api_key=steam_api_key)
    steamid = steamuserinfo.resolve_vanity_url("radekaadek", format="json")['response']['steamid']
    usersummary = steamuserinfo.get_player_summaries(steamid, format="json")['response']['players'][0]


    plik.write(str(usersummary))

    plik.close()

if __name__ == '__main__':
    main()
