# -*- coding:utf-8 -*-
__author__ = "ganbin"
import requests
from lxml import etree
from PIL import Image
import os
import http.cookiejar as cookielib
import json
import re


class ProxyPool(object):
    def __init__(self, need_save=True, need_validate=True, validate_length=50):
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        self.captcha_url = 'http://awmproxy.net/captcha.php'
        self.proxy_url = 'http://awmproxy.net/freeproxy.php'
        self.session.cookies = cookielib.LWPCookieJar(filename='proxy_cookies')
        self.xpath = '//*[@class="info3-inp"]/input/@value'
        self.need_save = need_save
        self.need_validate = need_validate
        self.validate_length = validate_length

    def load_cookies(self):
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print("Cookie 未能加载")
            self.session.get(self.proxy_url)
            self.session.cookies.save()

    def handle_captcha(self):
        self.load_cookies()
        captcha = self.session.get(self.captcha_url)
        with open('captcha.gif', 'wb') as f:
            f.write(captcha.content)
        try:
            im = Image.open('captcha.gif')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.gif'))
        captcha = input("please input the captcha\n>")
        return captcha

    def get_proxies_url(self):
        captcha = self.handle_captcha()
        param = {
            'captcha': captcha
        }
        response = self.session.post(url=self.proxy_url, data=param)
        selector = etree.HTML(response.text)
        try:
            proxies_url = selector.xpath(self.xpath)[0]
        except IndexError:
            print('xpath is wrong, please update')
            raise IndexError
        return proxies_url

    def produce_proxies(self):
        proxies_url = self.get_proxies_url()
        response = self.session.get(url=proxies_url)
        proxies = response.text
        if self.need_save:
            with open('freeproxies.txt', 'w') as f:
                f.write(proxies)
        return proxies

    def validate_proxies(self):
        proxies = self.produce_proxies()
        proxies = re.findall('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d+', proxies)
        validate_proxies = []
        for p in proxies[4173:]:
            proxies = {
                'https': 'http://%s' % (p),
            }
            try:
                r = requests.get('https://www.edmunds.com/',
                                 proxies=proxies, timeout=5)
            except Exception:
                print('bad ip', p)
                continue
            if r.status_code == requests.codes.ok:
                print('good ip', p)
                validate_proxies.append(p)
                if len(validate_proxies) > self.validate_length:
                    break
        with open('validate_proxies.txt', 'w') as f:
            json.dump(validate_proxies, f)


if __name__ == '__main__':
    proxy = ProxyPool(validate_length=50)
    proxy.validate_proxies()
