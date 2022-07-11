import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def data(username, session):
    site_url = f"https://www.snapchat.com/add/{username}"
    async with session.get(site_url) as response:
        match response.status:
            case 200:
                bs = BeautifulSoup(await response.text(), 'html.parser')
                profile_card = str(bs.find('span', class_ = 'UserDetailsCard_title__trfvf UserDetailsCard_oneLineTruncation__uhOF5').string)
                bitmoji_link = f'https://app.snapchat.com/web/deeplink/snapcode?username={username}&type=SVG&bitmoji=enable'
                print('snap done!')
                return {'profile_card': profile_card, 'bitmoji_link': bitmoji_link, 'error': 'OK'}
            case 404:
                return {'error': 'NOT_FOUND'}
            case _:
                return {'error': 'UNKNOWN_ERROR'}

