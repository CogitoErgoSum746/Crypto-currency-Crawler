# exchange_rates/items.py

import scrapy

class CryptoItem(scrapy.Item):
    rank = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
    price = scrapy.Field()
    volume_24h = scrapy.Field()
    market_cap = scrapy.Field()
