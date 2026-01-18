import ccxt
from datetime import datetime
class CoinService:
    _instance = None
    def __new__(cls):
        if cls._instance is None : # 아직 생성하지 않음
            cls._instance = super().__new__(cls) # 객체 생성하여 _instace에 할당
            cls._instance.__exchange = ccxt.upbit()
        return cls._instance
    def get_prices(self,symbols:list) :
        prices= {}
        try :
            tickers = self._instance.__exchange.fetch_tickers(symbols)
            for symbol in symbols:
                prices[symbol] = tickers[symbol]['last']
            return prices
        except Exception as e :
            print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")
            return {}
        
coin_service = CoinService()
my_coins = ['BTC/KRW', 'ETH/KRW', 'XRP/KRW']

prices = coin_service.get_prices(my_coins)
print(prices)