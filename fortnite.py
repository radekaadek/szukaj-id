import requests

fortnite_api_key = 'b4dab92b-ac98-4d0f-8cc9-5e2bc93de384'
fortnite_api_website = 'https://fortnite-api.com/v2/stats/br/v2'

#dokumentacja: https://dash.fortnite-api.com/endpoints/stats
#['image_url', 'raw_data', 'stats', 'user']
#[26:]
#.raw_data['all']['overall']['kd']
#'ninja' - niepubliczny

username = 'radekaadek'

def dane(username, platform='epic') -> dict:
    params = {'accountType': platform, 'name': username}
    headers = {'Authorization': fortnite_api_key}
    raw_response = requests.get(fortnite_api_website, params=params, headers=headers).json()
    if raw_response['status'] == 403:
        # players account stats are private
        return {'error': 'PRIVATE'}
    if raw_response['status'] == 404:
        # player not found
        return {'error': 'NOT_FOUND'}
    name = raw_response['data']['account']['name']
    print(raw_response['data']['account'])
    return {'error': 'OK', 'name': name, 'raw_data': raw_response['data']['account']}
    

dane(username)
