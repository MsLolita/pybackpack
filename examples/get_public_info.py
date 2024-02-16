import asyncio

from backpack import Backpack


async def main():
    # Put api keys if you want to use private api
    backpack = Backpack()

    response = await backpack.get_status()
    print(await response.json())  # {'message': None, 'status': 'Ok'}

    response = await backpack.get_ticker('BONK_USDC')
    print("Response:", await response.text())  # {"firstPrice":"0.00001406", ..., "volume":"334381691532"}

    await backpack.close()


if __name__ == '__main__':
    asyncio.run(main())
