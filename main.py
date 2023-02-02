import asyncio

import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from pyshorteners import Shortener

BASE_URL = 'https://www.trulia.com/FL/Tampa/'
HEADERS = {'User-Agent': UserAgent().random}


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            r = await aiohttp.StreamReader.read(response.content)
            soup = BS(r, 'html.parser')
            items = soup.find_all('div', class_="Box__BoxElement-sc-1f5rw0h-0 fEsbLJ PropertyCard__PropertyCardContainer-m1ur0x-4 kYIQmo")
            for item in items:
                title = item.find('a', class_="PropertyCard__StyledLink-m1ur0x-3 fiWGOD")
                link = title.get('href')
                price = item.find('div', class_="Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 enhvQK iilDhj").text.strip()
                short_link = Shortener().tinyurl.short(f'https://www.trulia.com{link}')

                print(f'PROPERTY ADDRESS: {title.text.strip()}; ------ PRICE: {price}; ------ LINK: {short_link}')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
