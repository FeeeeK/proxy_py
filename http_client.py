import json

import aiohttp
from aiohttp_socks import ProxyConnector
from fake_useragent import UserAgent

from proxy_py import settings


class HttpClientResult:
    text = None
    aiohttp_response = None

    @staticmethod
    async def make(aiohttp_response):
        obj = HttpClientResult()
        obj.aiohttp_response = aiohttp_response
        obj.text = await obj.aiohttp_response.text()

        return obj

    def as_text(self):
        return self.text

    def as_json(self):
        return json.loads(self.text)


user_agent = UserAgent()


# TODO: complete cookies saving
class HttpClient:
    """
    Simple class for making http requests,
    user-agent is set to random one in constructor
    """

    def __init__(self):
        self.user_agent = user_agent.random
        self.timeout = 60
        self.proxy_address = None

    async def get(self, url):
        """
        send HTTP GET request

        :param url:
        :return:
        """
        return await self.request("GET", url, None)

    async def post(self, url, data):
        """
        send HTTP POST request

        :param url:
        :param data:
        :return:
        """
        return await self.request("POST", url, data)

    async def request(self, method, url, data) -> HttpClientResult:
        headers = {
            "User-Agent": self.user_agent,
        }

        async with aiohttp.ClientSession(
            connector=ProxyConnector.from_url(self.proxy_address),
            connector_owner=False,
        ) as session:
            async with session.request(
                method,
                url=url,
                data=data,
                timeout=self.timeout,
                headers=headers,
            ) as response:
                return await HttpClientResult.make(response)


async def get_text(url):
    """
    fast method for sending get response without creating extra objects

    :param url:
    :return:
    """
    return (await HttpClient().get(url)).as_text()


async def get_json(url):
    return (await HttpClient().get(url)).as_json()
