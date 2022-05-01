from riotwatcher import LolWatcher, ApiError

#dokumentacja: https://riot-watcher.readthedocs.io/en/latest/index.html

riot_api_key = 'RGAPI-a59ca943-0182-4b2e-b3b1-5d06674b849d'
lol_watcher = LolWatcher(riot_api_key)

regiony = {'Brasil': 'BR1', 'Europe Nordic & East': 'EUN1', 'Europe West': 'EUW1', 'Japan': 'JP1', 'Korea': 'KR', 'Latin America North': 'LA1', 'Latin America South': 'LA2', 'North America': 'NA1', 'Oceania': 'OC1', 'Russia': 'RU', 'Turkey': 'TR1'}

def zwroc_region(nazwa_regionu):
    return regiony[nazwa_regionu]

def zwroc_uzytkownika(region, nazwa_uzytkownika):
        try:
            uzytkownik = lol_watcher.summoner.by_name(region, nazwa_uzytkownika)
            return uzytkownik
        except ApiError as err:
            return err.response.status_code
                

class player:
    def __init__(self, nazwa, region):
        self.nazwa = nazwa
        self.region = region
        self.uzytkownik = zwroc_uzytkownika(self.region, self.nazwa)
    def czy_istnieje(self):
        if self.uzytkownik == 404:
            return False
        elif self.uzytkownik == 429:
            return 'Zbyt dużo zapytań'
        else:
            return True

    # zwraca link do profilowego
    def avatar(self):
        return f'https://ddragon.leagueoflegends.com/cdn/10.18.1/img/profileicon/{self.uzytkownik["profileIconId"]}.png'

    # poziom gracza
    def poziom(self):
        return self.uzytkownik['summonerLevel']
    
    def czy_w_grze(self):
        try:
            lol_watcher.spectator.by_summoner(self.region, self.uzytkownik['id'])['gameId']
            return True
        except:
            return False

    def link_do_profilu(self):
        return {'link':f'https://{self.region}.op.gg/summoner/userName={self.nazwa}', "name1":self.nazwa,}

    # zwraca tier, range, lp, wygrane i przegrane
    def ranga(self):
        lista = lol_watcher.league.by_summoner(self.region, self.uzytkownik['id'])
        for element in lista:
            if element['queueType'] == 'RANKED_SOLO_5x5':
                return [element['tier'], element['rank'], element['leaguePoints'], element['wins'], element['losses']]
        return None
    


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
