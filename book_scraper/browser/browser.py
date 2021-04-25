from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup


class Async(object):
    async def __new__(cls, *arg, **kwarg):
        instance = super().__new__(cls)
        await instance.__init__(*arg, **kwarg)
        return instance

    async def __init__(obj):
        pass


class Browser(Async):
    async def __init__(self, url, *args, **kwargs):
        async with httpx.AsyncClient() as client:
            self.url = url
            response = await client.get(self.url)
            self.soup = BeautifulSoup(response.text, 'html.parser')

    async def go_to(self, url):
        async with httpx.AsyncClient() as client:
            url = self.clean_url(url)
            page = await client.get(url)
            self.soup = BeautifulSoup(page.text, 'html.parser')

    async def get(self, url):
        async with httpx.AsyncClient() as client:
            url = self.clean_url(url)
            return await client.get(url)

    def clean_url(self, url_to_clean):
        return urljoin(self.url, url_to_clean)
