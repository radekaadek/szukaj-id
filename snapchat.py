import profile
from urllib.request import urlopen
from bs4 import BeautifulSoup

username = 'marti1241'

site = f"https://www.snapchat.com/add/{username}"
html = urlopen(site)
bs = BeautifulSoup(html, 'html.parser')

profile_card = bs.find('span', class_ = 'UserDetailsCard_title__trfvf UserDetailsCard_oneLineTruncation__uhOF5')
elem=str(profile_card.string)
print(elem)
print(type(elem))

bitmoji_link = f'https://app.snapchat.com/web/deeplink/snapcode?username={username}&type=SVG&bitmoji=enable'

