from typing import Optional
import aiohttp

from .public import BackpackPublic
from .private import BackpackPrivate


class Backpack(BackpackPrivate, BackpackPublic):
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        super(Backpack, self).__init__(api_key, api_secret)

    def _init_session(self):
        return aiohttp.ClientSession()

    async def close(self):
        await self.session.close()
