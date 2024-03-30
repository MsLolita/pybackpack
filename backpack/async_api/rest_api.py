from typing import Optional
import aiohttp
from aiohttp_proxy import ProxyConnector

from .public import BackpackPublic
from .private import BackpackPrivate


class Backpack(BackpackPrivate, BackpackPublic):
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, proxy: Optional[str] = None):
        self.proxy = proxy

        super(Backpack, self).__init__(api_key, api_secret)

    def _init_session(self):
        return aiohttp.ClientSession(
            trust_env=True,
            connector=ProxyConnector.from_url(self.proxy, ssl=False) if self.proxy else aiohttp.TCPConnector(ssl=False)
        )

    async def close(self):
        await self.session.close()
