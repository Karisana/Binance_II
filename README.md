

live_data.py  -  собирает данные по нужной валюте в sql

live_tranding.py - работает по сценарию и сообщает о нужной покупке / продаже.

Сценарий: -- > Следим за валютой. 
          -- > Если валюта растет на x%.- покупаем  
          -- > Выходим, когда прибыль выше x% или ниже x%
          
apikey, secret из api (если вставлять свои, то прятать через dvenv) 

модули:
-- > sqlalchemy<2.0
-- > pandas
-- > binance
-- > asyncio
-- > nest_asyncio

Убрать лишние принты, они для удобства. 
