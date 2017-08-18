# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import json
from fake_useragent import UserAgent

class UserAgentMiddleWare(object):
    def __init__(self, crawler):
        super(UserAgentMiddleWare, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.meta['dont_redirect'] = True
        request.headers.setdefault('User-Agent', get_ua())



class EdmundsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#
# class HttpProxyMiddleware(object):
#     def __init__(self):
#         with open('validate_proxys.txt', 'r') as f:
#             r_json = json.loads(f.read())
#         self.proxy_list = [x.strip('\n') for x in r_json if x.strip('\n') != '']
#
#     def process_response(self, request, response, spider):
#         if response.status != 200:
#             https_proxy = 'https://%s' % random.choice(self.proxy_list)
#             request.meta['proxy'] = https_proxy
#             new_request = request.copy()
#             new_request.dont_filter = True
#             return new_request
#         else:
#             return response


class HttpProxyMiddleware(object):
    def __init__(self):
        with open('validate_proxys.txt', 'r') as f:
            rf = json.loads(f.read())
        self.proxies = [x.strip('\n') for x in rf]

    def process_response(self, request, response, spider):
        if response.status != 200:
            request.meta['proxy'] = "https://%s" % (random.choice(self.proxies))
            # request.meta['proxy'] = "http://138.0.50.123:53281"
            print(request.meta['proxy'])
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        else:
            return response


















