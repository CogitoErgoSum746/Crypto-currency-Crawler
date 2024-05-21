# # middlewares.py

# import scrapy
# import time

# class RotateProxyMiddleware:
#     def __init__(self, proxies):
#         self.proxies = proxies
#         self.current_proxy_index = 0

#     @classmethod
#     def from_crawler(cls, crawler):
#         proxies = getattr(crawler.settings, 'PROXIES', [])
#         return cls(proxies)

#     def process_request(self, request, spider):
#         if self.proxies:
#             request.meta['proxy'] = self.proxies[self.current_proxy_index]
#             self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
