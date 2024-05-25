import scrapy
from exchange_rates.items import CryptoItem

class TemplateSpider(scrapy.Spider):
    name = 'crypto_spider'

    def __init__(self, *args, **kwargs):
        super(TemplateSpider, self).__init__(*args, **kwargs)

        start_urls = ["https://www.coingecko.com"]
        # alt_start_url = "https://www.coinbase.com/en-gb/explore?page=1"

        for i in range(2,145):
            start_url = f"https://www.coingecko.com/?page={i}"
            start_urls.append(start_url)

        self.start_urls = start_urls
        # self.alt_start_url = alt_start_url

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        # 'HTTP_PROXY': 'http://69.58.2.135:3128',
        'PROXY_POOL_ENABLED': False,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 2,   
        'LOG_LEVEL': 'DEBUG',
    }

    handle_httpstatus_list = [500, 502, 503, 504, 522, 524, 400, 403, 404, 408, 429]

    def parse(self, response):
        # print(response.request.meta.get('proxy'))
        if response.status == 200:
            table = response.css('table tbody').get()
            rows = scrapy.Selector(text=table).css('tbody tr')

            for row in rows:
                item = CryptoItem()
                item['rank'] = row.css('td:nth-child(2)::text').get().strip()
                item['name'] = row.css('td:nth-child(3) div div:nth-child(1)::text').get().strip()
                item['code'] = row.css('td:nth-child(3) div div.tw-text-xs::text').get().strip()
                item['price'] = row.css('td:nth-child(5) span::text').get().strip()
                item['volume_24h'] = row.css('td:nth-child(10) span::text').get().strip()
                item['market_cap'] = row.css('td:nth-child(11) span::text').get().strip()

                yield item

            # yield scrapy.Request(self.alt_start_url, callback=self.parse_alt_link, dont_filter=True)

    def parse_alt_link(self, response):
        if response.status == 200:
            table = response.css('table tbody').get()
            rows = scrapy.Selector(text=table).css('tbody tr')
            # for row in rows:
            #         tp = row.css('td:nth-child(10) span::text').get().strip()    

            results = []
            # rows = response.css('table tbody tr')
            for row in rows:
                print(row.css('td:nth-child(3)::text').get().strip())
                # item = CryptoItem()
                # item['name'] = row.css('td:nth-child(3) div div:nth-child(1)::text').get().strip()
                # item['code'] = row.css('td:nth-child(3) div div.tw-text-xs::text').get().strip()

                # yield item