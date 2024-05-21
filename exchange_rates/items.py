# items.py

import scrapy

class ExchangeRateItem(scrapy.Item):
    base_currency = scrapy.Field()
    foreign_currency = scrapy.Field()
    exchange_rate = scrapy.Field()
    market_time = scrapy.Field()
