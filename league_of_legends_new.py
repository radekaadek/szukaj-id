import aiohttp
import asyncio

#dokumentacja: https://riot-watcher.readthedocs.io/en/latest/index.html

riot_api_key = 'RGAPI-30babb70-cf93-41b8-8e0c-32fb0fb543f2'

regiony = {'Brasil': 'BR1', 'Europe Nordic & East': 'EUN1', 'Europe West': 'EUW1', 'Japan': 'JP1', 'Korea': 'KR', 'Latin America North': 'LA1', 'Latin America South': 'LA2', 'North America': 'NA1', 'Oceania': 'OC1', 'Russia': 'RU', 'Turkey': 'TR1'}

def zwroc_region(nazwa_regionu):
    return regiony[nazwa_regionu]

def link_do_profilu(username, region):
    regiony_opgg = {'BR1': 'br', 'EUN1': 'eune', 'EUW1': 'euw', 'JP1': 'jp', 'KR': 'kr', 'LA1': 'lan', 'LA2': 'las', 'NA1': 'na', 'OC1': 'oc', 'RU': 'ru', 'TR1': 'tr'}
    return {'link':f'https://{regiony_opgg[region]}.op.gg/summoner/userName={username}', "name1":username,}


