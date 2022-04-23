import fortnite_api
import asyncio
from timeit import default_timer as timer
from datetime import timedelta

api = fortnite_api.FortniteAPI('b4dab92b-ac98-4d0f-8cc9-5e2bc93de384', True)
api_false = fortnite_api.FortniteAPI('b4dab92b-ac98-4d0f-8cc9-5e2bc93de384', False)

def main2():
    play = api.playlist.fetch_all()
    szop = api.shop.fetch()
    newsy = api.news.fetch()
    jezyk = api.map.fetch()
    staty = api.cosmetics.fetch_all()
    taski = [play, szop, newsy, jezyk, staty]
    return taski

def main2_false():
    play = api_false.playlist.fetch_all()
    szop = api_false.shop.fetch()
    newsy = api_false.news.fetch()
    jezyk = api_false.map.fetch()
    staty = api_false.cosmetics.fetch_all()
    return [play, szop, newsy, jezyk, staty]



async def main():
    odp = []
    start = timer()
    taski = main2()
    odpowiedzi = await asyncio.gather(*taski)
    for odpowiedz in odpowiedzi:
        odp.append(odpowiedz)
    print(odp)
    end = timer()
    print(timedelta(seconds=end-start))
    start = timer()
    sad = main2_false()
    print(sad)
    end = timer()
    print(timedelta(seconds=end-start))
    start = timer()
    play = api_false.playlist.fetch_all()
    end = timer()
    print(timedelta(seconds=end-start))


if __name__ == '__main__':
    asyncio.run(main())


