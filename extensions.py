import json
import requests
from config import currency


class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
            if quote == base:
                raise APIException('Невозможно конвертироваить одинаковые валюты')
                
            try:
                quote_ticker = currency[quote]
            except KeyError:
                raise APIException(f'Не удалось обработать валюту {quote}')
            
            try:
                base_ticker = currency[base]
            except KeyError:
                raise APIException(f'Не удалось обработать валюту {base}')
            
            try:
                amount = float(amount)
            except ValueError:
                raise APIException(f'Не удалось обработать количество {amount}')


            r = requests.get(f'https://api.apilayer.com/fixer/latest?base=USD&symbols={quote_ticker},{base_ticker}', headers={'apikey':'80fEz4bNx26ZoRJa2xgZ1RIj5SLR8ViF'}).content
            r = json.loads(r)
            total_base = r["rates"][currency[base]] / r["rates"][currency[quote]] * float(amount)
            return total_base