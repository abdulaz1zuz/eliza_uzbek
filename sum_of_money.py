from decimal import Decimal
a=1.2
sell_price = Decimal(a)
buy_price = Decimal('232.99')
items_sold = Decimal('1e18')
profit = (sell_price - buy_price)
print(sell_price)
