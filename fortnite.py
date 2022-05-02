import fortnite_api

api = fortnite_api.FortniteAPI('b4dab92b-ac98-4d0f-8cc9-5e2bc93de384')

#dokumentacja: https://dash.fortnite-api.com/endpoints/stats
#['image_url', 'raw_data', 'stats', 'user']
#[26:]
#.raw_data['all']['overall']['kd']
#'ninja' - niepubliczny


class Gracz_fortnite:
    def __init__(self, username, platform='epic'):
        self.username = username
        self.platform = platform
        try:
            self.player_base = api.stats.fetch_by_name(username).raw_data
            self.player = self.player_base['stats']['all']['overall']
        except Exception as error:
            self.player_base = error
            self.player = error
            

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


