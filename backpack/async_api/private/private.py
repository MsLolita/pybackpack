import base64
import time
from typing import Callable, Optional
from urllib.parse import urlencode

import aiohttp
import ed25519

from backpack.base.models import BaseClient


class BackpackPrivate(BaseClient):
    def __init__(self, api_key: str, api_secret: str):  # api_key is unnecessary
        super().__init__()

        if api_key is not None and api_secret is None:
            raise ValueError('api_secret must be provided if api_key is provided')
        if api_secret is not None:
            self.private_key = ed25519.SigningKey(base64.b64decode(api_secret))
            self.verifying_key = self.private_key.get_verifying_key()
            self.verifying_key_b64 = base64.b64encode(self.verifying_key.to_bytes()).decode()

    def _sign_request(self, instruction: str, body: Optional[dict] = None):
        """
        Sign a request with the given instruction and optional parameters.

        Args:
            instruction (str): The instruction for the request.
            body (Optional[dict]): Optional parameters for the request.

        Returns:
            dict: A dictionary containing the signed request data.
        """

        timestamp = str(int(time.time() * 1000))
        window = '5000'

        body = {
            'instruction': instruction,
            **dict(sorted((body or {}).items())),
            'timestamp': timestamp,
            'window': window,
        }
        message = urlencode(body)
        signature = self.private_key.sign(message.encode())
        signature_b64 = base64.b64encode(signature).decode()

        return {
            'X-API-KEY': self.verifying_key_b64,
            'X-TIMESTAMP': timestamp,
            'X-WINDOW': window,
            'Content-Type': 'application/json',
            'X-SIGNATURE': signature_b64
        }

    @staticmethod
    def sign_request(instruction: str):
        """
        A decorator that signs a request with the given instruction before executing the wrapped function.

        Args:
            instruction (str): The instruction to sign the request.

        Returns:
            Callable: The wrapped function with the signing logic.
        """

        def decorator(func: Callable):
            async def wrapper(self: 'BackpackPrivate', *args, **kwargs):
                body = kwargs.get('payload') or kwargs.get('params')
                headers = self._sign_request(instruction, body)
                return await func(self, headers=headers, *args, **kwargs)

            return wrapper

        return decorator

    async def get_balances(self):
        """
        Retrieves account balances and the state of the balances (locked or available).
        Locked assets are those that are currently in an open order.

        https://docs.backpack.exchange/#tag/Capital/operation/get_balances

        :return:
        """

        url = self.API_URL + '/api/v1/capital'

        headers = self._sign_request('balanceQuery')

        return await self.session.get(url, headers=headers)

    async def get_deposits(self, limit: int = 100, offset: int = 0):
        """
        Retrieves deposit history.

        https://docs.backpack.exchange/#tag/Capital/operation/get_deposits

        :return:
        """

        url = self.API_URL + '/wapi/v1/capital/deposits'

        params = {
            'limit': limit,
            'offset': offset
        }

        headers = self._sign_request('balanceQuery', body=params)

        return await self.session.get(url, headers=headers, params=params)

    async def get_deposit_address(self, blockchain: str) -> aiohttp.ClientResponse:
        """
        Retrieves deposit address for the given asset.

        https://docs.backpack.exchange/#tag/Capital/operation/get_deposit_address

        :return:
        """

        url = self.API_URL + '/wapi/v1/capital/deposit/address'

        params = {
            'blockchain': blockchain.capitalize()
        }

        headers = self._sign_request('depositAddressQuery', body=params)

        return await self.session.get(url, headers=headers, params=params)

    async def get_withdrawals(self, limit: int = 100, offset: int = 0):
        """
        Retrieves withdrawal history.

        https://docs.backpack.exchange/#tag/Capital/operation/get_withdrawals

        :return:
        """

        url = self.API_URL + '/wapi/v1/capital/withdrawals'

        params = {
            'limit': limit,
            'offset': offset
        }

        headers = self._sign_request('withdrawalQueryAll', body=params)

        return await self.session.get(url, headers=headers, params=params)

    async def request_withdrawal(self, address: str, blockchain: str, quantity: str, symbol: str,
                                 client_id: Optional[int] = None,
                                 two_factor_token: Optional[str] = None):
        """
        Sends a withdrawal request to the specified address.

        https://docs.backpack.exchange/#tag/Capital/operation/request_withdrawal

        :return:
        """

        url = self.API_URL + '/wapi/v1/capital/withdraw'

        payload = {
            'address': address,
            'blockchain': blockchain.capitalize(),
            'quantity': quantity,
            'symbol': symbol
        }

        if client_id:
            payload['clientId'] = client_id

        if two_factor_token:
            payload['twoFactorToken'] = two_factor_token

        headers = self._sign_request('withdraw', body=payload)

        return await self.session.post(url, headers=headers, json=payload)

    async def get_order_history(self, symbol: str, limit: int = 100, offset: int = 0):
        """
        Retrieves the order history for the user.
        This includes orders that have been filled and are no longer on the book.
        It may include orders that are on the book, but the /orders endpoint contains more up-to-date data.

        https://docs.backpack.exchange/#tag/History/operation/get_order_history

        :param symbol:
        :param limit:
        :param offset:
        :return:
        """

        url = self.API_URL + '/wapi/v1/history/orders'

        params = {
            'symbol': symbol,
            'limit': limit,
            'offset': offset
        }

        headers = self._sign_request('orderHistoryQueryAll', body=params)

        return await self.session.get(url, headers=headers, params=params)

    async def get_fill_history(self, order_id: str, symbol: str, limit: int = 100, offset: int = 0):
        """
        Retrieves historical fills, with optional filtering for a specific order or symbol.

        https://docs.backpack.exchange/#tag/History/operation/get_fills

        :param order_id:
        :param symbol:
        :param limit:
        :param offset:
        :return:
        """

        url = self.API_URL + '/wapi/v1/history/fills'

        params = {
            'orderId': order_id,
            'symbol': symbol,
            'limit': limit,
            'offset': offset
        }

        headers = self._sign_request('fillHistoryQueryAll', body=params)

        return await self.session.get(url, headers=headers, params=params)

    async def get_open_order(self, symbol: str, client_id: int = None, order_id: str = None):
        """
        Retrieves an open order from the order book.
        This only returns the order if it is resting on the order book
        (i.e. has not been completely filled, expired, or cancelled).
        One of orderId or clientId must be specified. If both are specified, then orderId takes precedence.

        https://docs.backpack.exchange/#tag/Order/operation/get_order

        :return:
        """

        url = self.API_URL + '/api/v1/order'

        params = {
            'symbol': symbol
        }

        if client_id:
            params['clientId'] = client_id

        if order_id:
            params['orderId'] = order_id

        headers = self._sign_request('orderQuery', body=params)

        return await self.session.get(url, headers=headers, params=params)

    async def execute_order(
            self,
            symbol: str,
            side: str,
            order_type: str,
            price: Optional[str] = None,
            client_id: Optional[int] = None,
            quantity: Optional[str] = None,
            quote_quantity: Optional[str] = None,
            post_only: Optional[bool] = None,
            self_trade_prevention: Optional[str] = None,
            time_in_force: Optional[str] = None,
            trigger_price: Optional[str] = None
    ):
        """
        Submits an order to the matching engine for execution.

        https://docs.backpack.exchange/#tag/Order/operation/execute_order

        :return:
        """
        url = self.API_URL + '/api/v1/order'

        payload = {
            "clientId": client_id,
            "orderType": order_type.capitalize(),
            "postOnly": post_only,
            "price": price,
            "quantity": quantity,
            "quoteQuantity": quote_quantity,
            "selfTradePrevention": self_trade_prevention,
            "side": side.capitalize(),
            "symbol": symbol.upper(),
            "timeInForce": time_in_force,
            "triggerPrice": trigger_price
        }

        # remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        headers = self._sign_request('orderExecute', body=payload)

        return await self.session.post(url, headers=headers, json=payload)

    async def cancel_open_order(self, symbol: str, client_id: int = None, order_id: str = None):
        """
        Cancels an open order from the order book.
        One of orderId or clientId must be specified. If both are specified, then orderId takes precedence.

        https://docs.backpack.exchange/#tag/Order/operation/cancel_order

        :return:
        """

        url = self.API_URL + '/api/v1/order'

        params = {
            'symbol': symbol
        }

        if client_id:
            params['clientId'] = client_id

        if order_id:
            params['orderId'] = order_id

        headers = self._sign_request('orderCancel', body=params)

        return await self.session.delete(url, headers=headers, json=params)

    async def get_open_orders(self, symbol: str):
        """
        Retrieves all open orders. If a symbol is provided, only open orders for that market will be returned,
        otherwise all open orders are returned.

        https://docs.backpack.exchange/#tag/Order/operation/get_orders

        :return:
        """

        url = self.API_URL + '/api/v1/orders'

        params = {
            'symbol': symbol,
        }

        headers = self._sign_request('orderQueryAll', body=params)

        return await self.session.get(url, headers=headers, params=params)

    async def cancel_all_orders(self, symbol: str):
        """
        Cancels all open orders on the specified market.

        https://docs.backpack.exchange/#tag/Order/operation/cancel_open_orders

        :return:
        """

        url = self.API_URL + '/api/v1/orders'

        params = {
            'symbol': symbol,
        }

        headers = self._sign_request('orderCancelAll', body=params)

        return await self.session.delete(url, headers=headers, json=params)
