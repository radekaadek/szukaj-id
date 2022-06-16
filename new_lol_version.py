def main():
    with open('lol_version.txt', 'w') as f:
        f.write(str(requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]))

if __name__ == '__main__':
    main()
