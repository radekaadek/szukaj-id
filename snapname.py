import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def data(username, session):
    site_url = f"https://www.snapchat.com/add/{username}"
    async with session.get(site_url) as response:
        match response.status:
            case 200:
                r = await response.text()
                with open ("snapchat.html", "w", encoding="utf-8") as f:
                    f.write(str(r))
                
                bs = BeautifulSoup(r, 'html.parser')
                profile_card = str(bs.find('title').string)
                profile_card = profile_card.split('(', 1)[0]
                bitmoji_link = f'https://app.snapchat.com/web/deeplink/snapcode?username={username}&type=SVG&bitmoji=enable'
                return {'profile_card': profile_card, 'bitmoji_link': bitmoji_link, 'error': 'OK'}
            case 404:
                return {'error': 'NOT_FOUND'}
            case _:
                return {'error': 'UNKNOWN_ERROR'}

