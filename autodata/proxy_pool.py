# -*- coding:utf-8 -*-
__author__ = "ganbin"
import requests
import re
import settings


class ProxyPool(object):
    def __init__(self, need_save=True, need_validate=True):
        self.validate_length = settings.VALIDATE_LENGTH
        self.validate_url = settings.VALIDATE_URL

    def validate_proxies(self):
        with open('freeproxies.txt', 'r') as f:
            proxies = f.read()
        proxies = re.findall('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d+', proxies)
        validate_proxies = []
        with open('validate_proxies.txt', 'a') as f:
            for p in proxies:
                proxies = {
                    'https': 'http://%s' % (p),
                }
                try:
                    r = requests.get(self.validate_url,
                                     proxies=proxies, timeout=5)
                except Exception:
                    print('bad ip', p)
                    continue
                if r.status_code == requests.codes.ok:
                    print('good ip', p)
                    validate_proxies.append(p)
                    f.write(p + '\n')
                    if len(validate_proxies) > self.validate_length:
                        break

if __name__ == '__main__':
    proxy = ProxyPool()
    proxy.validate_proxies()
