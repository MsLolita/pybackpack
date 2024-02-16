import asyncio
import random

from backpack import Backpack


async def main():
    # Put api key if you want to use private api
    backpack = Backpack('0sd20udO/0KEQZ23dGpBDPjct/t8fasTnro9u20eA=', 'gTdFa7YJAn6sd21kbYoPKQ1+/uiuMsd217GlXs23M=')

    response = await backpack.cancel_all_orders('BONK_USDC')
    print("Canceled orders:", await response.text())

    symbol = "BONK_USDC"
    client_id = random.randint(1, 9999)

    # create order
    order_details = {
        "client_id": client_id,  # not required
        "order_type": "Limit",  # ONLY LIMIT ORDERS working on exchange
        "price": "0.0000130",
        "quantity": "729",
        "side": "Bid",  # Bid - buy, Ask - sell
        "symbol": symbol,
    }

    response = await backpack.execute_order(**order_details)
    print("Created order:", await response.text())

    # get open order
    response = await backpack.get_open_order(symbol, client_id=client_id)
    print("Get this order:", await response.text())

    print("Waiting for 3 seconds and canceling order...")
    await asyncio.sleep(3)

    # cancel order
    response = await backpack.cancel_open_order(symbol, client_id=client_id)
    print("Canceled order:", await response.text())

    await backpack.close()


if __name__ == '__main__':
    asyncio.run(main())
