import scrapy
from exchange_rates.items import ExchangeRateItem
import re
import datetime

class TemplateSpider(scrapy.Spider):
    name = 'crypto_spider'

    def __init__(self, *args, **kwargs):
        super(TemplateSpider, self).__init__(*args, **kwargs)
        
        # Load cryptos from text file
        with open('cryptos.txt') as f:
            cryptos = f.read().splitlines()

        # start_urls = ["https://www.forbes.com/advisor/money-transfer/currency-converter/cad-btc/"]
        start_urls = []

        # Generate the start URLs
        for i in range(len(cryptos)):
            for j in range(len(cryptos)):
                if i != j:
                    # start_url = f"https://wise.com/in/currency-converter/{countries[i]}-to-{countries[j]}-rate?"
                    start_url = f"https://www.forbes.com/advisor/money-transfer/currency-converter/{cryptos[i]}-{cryptos[j]}/"
                    start_urls.append(start_url)

        self.start_urls = start_urls

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
            exchange_rate_raw = response.css('div.hero-template_content h2 strong::text').get()
            market_time_raw = response.css('div.hero-template_content h2 time::text').get()

            pattern = r'\d+\.\d{2}'
            match = re.search(pattern, exchange_rate_raw)
            exchange_rate = match.group()

            market_time_str = datetime.datetime.strptime(market_time_raw, "%b %d, %Y %H:%M %Z")
            market_time = market_time_str.strftime("%H:%M:%S")

            base_currency, foreign_currency = self.extract_currencies(response.url)
            print(base_currency,foreign_currency)
            yield ExchangeRateItem(base_currency=base_currency, foreign_currency=foreign_currency, exchange_rate=exchange_rate, market_time=market_time)
        else:
            base_currency, foreign_currency = self.extract_currencies(response.url)
            alt_start_url = f"https://valuta.exchange/{base_currency.upper()}-to-{foreign_currency.upper()}?"
            yield scrapy.Request(alt_start_url, callback=self.parse_alt_link,
                                  meta={'base_currency': base_currency, 'foreign_currency': foreign_currency}, dont_filter=True)

    def extract_currencies(self, url):
        parts = url.rstrip('/').split('/')
        currency_part = parts[-1]
        currencies = currency_part.split('-')

        if len(currencies) == 2:
            return currencies
        else:
            return None, None

    def parse_alt_link(self, response): 
        if response.status == 200:
            exchange_rate = response.css('div.UpdateTime__Container-sc-136xv3i-0.gMmDCR span.UpdateTime__ExchangeRate-sc-136xv3i-1.djCdnS::text').get()
            market_time_raw = response.css('small.m-r-1::text').get()
            pattern = r'at (\d{2}:\d{2})$'
            match = re.search(pattern, market_time_raw)
            market_time_str = match.group(1)  # Extract the time value

            try:
                # Parse the time string assuming HH:MM format
                time_obj = datetime.datetime.strptime(market_time_str, "%H:%M")
            except ValueError:
                # Handle invalid time format
                return None
            
            market_time = time_obj.strftime("%H:%M:%S")

            base_currency, foreign_currency = self.extract_currencies(response.url)
            yield ExchangeRateItem(base_currency=base_currency, foreign_currency=foreign_currency, exchange_rate=exchange_rate, market_time=market_time)
        else:
            base_currency = response.meta['base_currency']
            foreign_currency = response.meta['foreign_currency']
            alt_start_url = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From={base_currency.upper()}&To={foreign_currency.upper()}"
            yield scrapy.Request(alt_start_url, callback=self.parse_xe_link,
                                  meta={'base_currency': base_currency, 'foreign_currency': foreign_currency}, dont_filter=True)
            
    def parse_xe_link(self, response):
        if response.status == 200:
            mangea_rate = response.css('main.tab-box__ContentContainer-sc-28io75-3.joNDZm p.result__BigRate-sc-1bsijpp-1.dPdXSB::text').get()
            faded_digits = response.css('main.tab-box__ContentContainer-sc-28io75-3.joNDZm p.result__BigRate-sc-1bsijpp-1.dPdXSB span.faded-digits::text').get()
            market_time_raw = response.css('small.m-r-1::text').get()
            pattern = r'at (\d{2}:\d{2})$'
            match = re.search(pattern, market_time_raw)
            market_time_str = match.group(1)  # Extract the time value

            try:
                # Parse the time string assuming HH:MM format
                time_obj = datetime.datetime.strptime(market_time_str, "%H:%M")
            except ValueError:
                # Handle invalid time format
                return None
            
            market_time = time_obj.strftime("%H:%M:%S")
                        
            if mangea_rate and faded_digits:
                exchange_rate = mangea_rate + faded_digits
                base_currency, foreign_currency = self.extract_currencies(response.url)
                yield ExchangeRateItem(base_currency=base_currency, foreign_currency=foreign_currency, exchange_rate=exchange_rate, market_time=market_time)