import asyncio
import aiohttp

username = 'gabelogannewell'
steam_api_key = 'EE03692ACB03E4371522180E26926643'

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main(username):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/', params=params) as resp:
            data = await resp.json()
            steamid = data['response']['steamid']



if __name__ == '__main__':
    asyncio.run(main(username))
