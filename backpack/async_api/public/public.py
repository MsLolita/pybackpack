from backpack.base.models import BaseClient, Interval


class BackpackPublic(BaseClient):
    def __init__(self):
        super().__init__()

    async def get_assets(self):
        """
        Retrieves all the assets that are supported by the exchange.

        https://docs.backpack.exchange/#tag/Markets/operation/get_assets

        :return:
        """

        url = self.API_URL + '/api/v1/assets'

        return await self.session.get(url)

    async def get_markets(self):
        """
        Retrieves all the markets that are supported by the exchange.

        https://docs.backpack.exchange/#tag/Markets/operation/get_markets

        :return:
        """

        url = self.API_URL + '/api/v1/markets'

        return await self.session.get(url)

    async def get_ticker(self, symbol: str):
        """
        Retrieves summarised statistics for the last 24 hours for the given market symbol.

        https://docs.backpack.exchange/#tag/Markets/operation/get_ticker

        :param symbol:
        :return:
        """

        url = self.API_URL + '/api/v1/ticker'

        params = {
            'symbol': symbol
        }

        return await self.session.get(url, params=params)

    async def get_tickers(self):
        """
        Retrieves summarised statistics for the last 24 hours for all market symbols.

        https://docs.backpack.exchange/#tag/Markets/operation/get_tickers

        :return:
        """

        url = self.API_URL + '/api/v1/tickers'

        return await self.session.get(url)

    async def get_order_book_depth(self):
        """
        Retrieves the order book depth for a given market symbol.

        https://docs.backpack.exchange/#tag/Markets/operation/get_depth

        :return:
        """

        url = self.API_URL + '/api/v1/depth'

        return await self.session.get(url)

    async def get_k_lines(self, symbol: str, interval: Interval, start_time: int, end_time: int):
        """
        Get K-Lines for the given market symbol, optionally providing a startTime and endTime.
        If no startTime is provided, the interval duration will be used.
        If no endTime is provided, the current time will be used.

        https://docs.backpack.exchange/#tag/Markets/operation/get_klines

        :param symbol:
        :param interval:
        :param start_time:
        :param end_time:
        :return:
        """

        url = self.API_URL + '/api/v1/klines'

        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': end_time
        }

        return await self.session.get(url, params=params)

    async def get_status(self):
        """
        Get the system status, and the status message, if any.

        https://docs.backpack.exchange/#tag/System/operation/get_status

        :return:
        """

        url = self.API_URL + '/api/v1/status'

        return await self.session.get(url)

    async def send_ping(self):
        """
        Responds with pong.

        https://docs.backpack.exchange/#tag/System/operation/ping

        :return:
        """

        url = self.API_URL + '/api/v1/ping'

        return await self.session.get(url)

    async def get_system_time(self):
        """
        Get the system time.

        https://docs.backpack.exchange/#tag/System/operation/get_time

        :return:
        """

        url = self.API_URL + '/api/v1/time'

        return await self.session.get(url)

    async def get_recent_trades(self, symbol: str, limit: int = 100):
        """
        Retrieve the most recent trades for a symbol.
        This is public data and is not specific to any account. The maximum available recent trades is 1000.
        If you need more than 1000 trades use the historical trades endpoint.

        https://docs.backpack.exchange/#tag/Trades/operation/get_recent_trades

        :param symbol:
        :param limit:
        :return:
        """

        url = self.API_URL + '/api/v1/trades'

        params = {
            'symbol': symbol,
            'limit': limit
        }

        return await self.session.get(url, params=params)

    async def get_historical_trades(self, symbol: str, limit: int = 100, offset: int = 0):
        """
        Retrieves all historical trades for the given symbol.
        This is public trade data and is not specific to any account.

        https://docs.backpack.exchange/#tag/Trades/operation/get_historical_trades

        :return:
        """

        url = self.API_URL + '/api/v1/trades/history'

        params = {
            'symbol': symbol,
            'limit': limit,
            'offset': offset
        }

        return await self.session.get(url, params=params)

    async def close(self):
        await self.session.close()
