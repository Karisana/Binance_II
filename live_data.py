import asyncio
from binance import AsyncClient, BinanceSocketManager
import pandas as pd
import sqlalchemy

import nest_asyncio

nest_asyncio.apply()

symbol = 'BTCUSDT'

engine = sqlalchemy.create_engine('sqlite:///' + symbol + 'data.db')


def create_frame(res):
    df = pd.DataFrame([res])
    df = df[['s', 'E', 'p']]
    df.columns = ['symbol', 'Time', 'Price']

    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')

    return df


async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)

    ts = bm.trade_socket(symbol)  # тянуться данные для валюты

    async with ts as tscm:
        while True:
            res = await tscm.recv()
            # print(res)
            df = create_frame(res)
            df.to_sql(symbol, engine, if_exists='append', index=False)
            print(df)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
