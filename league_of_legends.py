from riotwatcher import LolWatcher, ApiError

#dokumentacja: https://riot-watcher.readthedocs.io/en/latest/index.html

riot_api_key = 'RGAPI-143972a8-d32e-433f-936f-05e727ec1af3'
lol_watcher = LolWatcher(riot_api_key)

regiony = {'Brasil': 'BR1', 'Europe Nordic & East': 'EUN1', 'Europe West': 'EUW1', 'Japan': 'JP1', 'Korea': 'KR', 'Latin America North': 'LA1', 'Latin America South': 'LA2', 'North America': 'NA1', 'Oceania': 'OC1', 'Russia': 'RU', 'Turkey': 'TR1'}

def zwroc_region(nazwa_regionu):
    return regiony[nazwa_regionu]

def zwroc_uzytkownika(region, nazwa_uzytkownika):
        try:
            uzytkownik = lol_watcher.summoner.by_name(region, nazwa_uzytkownika)
            return uzytkownik
        except ApiError as err:
            return "Error with code {}: {}".format(err.response.status_code, err.message)

class player:
    def __init__(self, nazwa, region):
        self.nazwa = nazwa
        self.region = region
        self.uzytkownik = zwroc_uzytkownika(self.region, self.nazwa)
    # zwraca link do profilowego
    def avatar(self):
        return f'https://ddragon.leagueoflegends.com/cdn/10.18.1/img/profileicon/{self.uzytkownik["profileIconId"]}.png'

    # poziom gracza
    def poziom(self):
        return self.uzytkownik['summonerLevel']

    # zwraca tier, range, lp, wygrane i przegrane
    def ranga(self):
        lista = lol_watcher.league.by_summoner(self.region, self.uzytkownik['id'])
        for element in lista:
            if element['queueType'] == 'RANKED_SOLO_5x5':
                return [element['tier'], element['rank'], element['leaguePoints'], element['wins'], element['losses']]
        return 'Nie znaleziono rangi'
    


# For Riot's API, the 404 status code indicates that the requested data wasn't found and
# should be expected to occur in normal operation, as in the case of a an
# invalid summoner name, match ID, etc.
#
# The 429 status code indicates that the user has sent too many requests
# in a given amount of time ("rate limiting").

# my_region = 'eun1'

# try:
#     response = lol_watcher.summoner.by_name(my_region, 'radekaadek')
# except ApiError as err:
#     if err.response.status_code == 429:
#         print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
#         print('this retry-after is handled by default by the RiotWatcher library')
#         print('future requests wait until the retry-after time passes')
#     elif err.response.status_code == 404:
#         print('Summoner with that ridiculous name not found.')
#     else:
#         raise
