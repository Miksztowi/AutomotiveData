# -*- coding:utf-8 -*-
import requests
import os
import json
import subprocess

if __name__ == '__main__':
    with open('../freeproxy.txt', 'r') as f:
        rf = f.readlines()
    proxy_list = [ x.strip('\n') for x in rf if x.strip('\n') != '']
    validate_proxt = []

    for p in proxy_list[60:]:
        proxies = {
            'https': 'http://%s' %(p),
            # 'https': 'http://%s:%s' % (ip, port),
        }
        try:
            r = requests.get('https://www.edmunds.com/',
                         proxies=proxies, timeout=3)
        except Exception:
            continue

        if r.status_code == requests.codes.ok:
            print(p)
            validate_proxt.append(p)
            if len(validate_proxt) > 10:
                break


    with open('validate_proxys.txt', 'w') as f:
        json.dump(validate_proxt, f)
