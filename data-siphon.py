from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter

c = CurrencyRates()
b = BtcConverter()

#USD TO EURO
usd = c.get_rate('USD', 'EUR')
#Bitcoin IN EURO
btc = b.get_latest_price('EUR')

print("Price of US Dolar in Euro: ", usd)
print("Price of Bitcoin in Euro: ", btc)