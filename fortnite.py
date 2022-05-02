import fortnite_api

api = fortnite_api.FortniteAPI('b4dab92b-ac98-4d0f-8cc9-5e2bc93de384')


#['image_url', 'raw_data', 'stats', 'user']
#[26:]
#.raw_data['all']['overall']['kd']
#'ninja' - niepubliczny

print(dir(api.stats.fetch_by_name('elyzy').stats)[26:])
print(api.stats.fetch_by_name('elyzy').raw_data)

class bekazapi:
    def __init__(self, platforma):
        self.platforma = platforma
    def value(self):
        return self.platforma



class Gracz_fortnite:
    def __init__(self, username, platform='epic'):
        self.username = username
        self.platform = platform
        self.player_base = api.stats.fetch_by_name(username, platform).raw_data
        self.player = self.player_base['stats']['all']['overall']
    
    def player_name(self):
        return self.player_base['account']['name']

    def battle_pass_level(self):
        return self.player_base['battlePass']['level']

    def kd(self):
        return self.player['kd']
    
    def minutesplayed(self):
        return self.player['minutesPlayed']
    
    def last_played(self):
        return self.player['lastModified']
    
    
x = Gracz_fortnite('elyzy')

print(x.battle_pass_level())
