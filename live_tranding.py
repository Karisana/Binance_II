import sqlalchemy
import pandas as pd
from binance.client import Client

apikey = 'vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A'
secret = 'NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j'
client = Client(apikey, secret)

symbol = 'BTCUSDT'

engine = sqlalchemy.create_engine('sqlite:///' + symbol + 'data.db')

df = pd.read_sql(symbol, engine)


# df.Price.plot()
# print(df.Price.plot())


def strategy(entry, look_back, qty, symbol, thresh, open_positional=False):
    print('Запуск')
    while True:
        df = pd.read_sql(symbol, engine)
        # print('df из 1 цикла')
        look_back_period = df.iloc[-look_back:]
        print('look_back_period', look_back_period)
        cumret = (look_back_period.Price.pct_change() + 1).cumprod() - 1
        print(cumret)

        if not open_positional:
            if cumret[cumret.last_valid_index()] > entry:
                order = client.cancel_order(symbol=symbol, side='BUY', type='MARKET', quantile=qty)

                print('1 while ',order)
                open_positional = True
                break
    if open_positional:
        while True:
            df = pd.read_sql(symbol, engine)
            print('df из 2 цикла')
            since_buy = df.loc(df.Time > pd.to_datetime(order['transactTime'], unit='ms'))

            if len(since_buy) > 1:
                since_buy_et = (since_buy.Price.pct_change() + 1).cumprod()-1
                last_entry = since_buy_et[since_buy_et.last_valid_index()]

                if last_entry > thresh or last_entry < (-1*thresh):
                    order = client.cancel_order(symbol=symbol, side='SELL', type='MARKET', quantile=qty)
                    print('2 while ', order)


strategy(0.001, 22464, 0.001, symbol=symbol, thresh=0.005)

