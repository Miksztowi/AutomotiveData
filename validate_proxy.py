# -*- coding:utf-8 -*-
__author__ = "ganbin"
import requests
import os
import json

if __name__ == '__main__':
    with open('../freeproxy.txt', 'r') as f:
        rf = f.readlines()
    proxy_list = [ x.strip('\n') for x in rf if x.strip('\n') != '']
    validate_proxt = []

    for p in proxy_list:
        ip = p.split(':')[0]
        port = p.split(':')[1]
        proxies = {
            'https': 'http://%s:%s' % (ip, port),
            # 'https': 'http://%s:%s' % (ip, port),
        }
        try:
            r = requests.get('https://httpbin.org/get?show_env=1',
                         proxies=proxies, timeout=5)
        except Exception:
            continue

        if r.status_code == requests.codes.ok:
            print(ip, port)
            validate_proxt.append(p)

    with open('validate_proxys.txt', 'w') as f:
        json.dump(proxy_list, f)
