import fortnite_api
import asyncio
from platform import system
if system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

typy_kont = {'pc': 'epic', 'psn': 'psn', 'xbl': 'xbl'}

api = fortnite_api.FortniteAPI('b4dab92b-ac98-4d0f-8cc9-5e2bc93de384', False)


def player_stats(name, platform):
    stats = api.stats.fetch_by_name(name, platform)
    return stats

print(player_stats('Krzysztof', 'epic'))
