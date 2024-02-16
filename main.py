import asyncio

from backpack import Backpack


async def main():
    # Put api key if you want to use private api
    # '0sd20udO/0KEQZ23dGpBDPjct/t8fasTnro9u20eA=	', 'gTdFa7YJAn6sd21kbYoPKQ1+/uiuMsd217GlXs23M='
    backpack = Backpack(api_secret='qRsjYJAn6lKdBNpkbYoPKQ1+/uiuMrY51BnhjlX35AM=')

    # public api, no need API Keys
    response = await backpack.get_status()
    print(await response.json())  # {'message': None, 'status': 'Ok'}

    response = await backpack.get_ticker('BONK_USDC')
    print("Response:", await response.text())  # {"firstPrice":"0.00001406", ..., "volume":"334381691532"}

    # # private api, need API Keys
    # resp = await backpack.()
    # print(await resp.json())  # {'message': None, 'status': 'Ok'}

    # public
    # a = await backpack.get_orderbook('BONK_USDC')
    # print("Response:", await a.text())
    # a = await backpack.cancel_all_orders('BONK_USDC')
    # print("Response:", await a.text())

    # private
    # order_details = {
    #     "client_id": 122522,
    #     "order_type": "Limit",
    #     "price": "0.0000137",
    #     "quantity": "729",
    #     # "post_only": True,
    #     # "selfTradePrevention": "RejectTaker",
    #     "side": "Bid",
    #     "symbol": "BONK_USDC",
    #     # "timeInForce": "GTC",
    # }
    # response = await backpack.cancel_open_order("BONK_USDC", client_id=122522)
    # print("Response:", await response.text())
    #
    await backpack.close()


if __name__ == '__main__':
    asyncio.run(main())
