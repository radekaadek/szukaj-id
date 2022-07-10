from bs4 import BeautifulSoup
import requests

# Fetch the page and create a Beautiful Soup object
page = requests.get("https://www.snapchat.com/add/marti1241")
soup = BeautifulSoup(page.text, "html.parser")

print(soup.encode('utf-8'))

# Locate every div tags that has class name of "UserCard_container__A4JCG"
s = soup.find_all("div", class_="UserCard_container__A4JCG", encoding='utf-8')
print(s)