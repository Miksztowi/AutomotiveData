# -*- coding:utf-8 -*-
import requests
import os
import json
import subprocess

if __name__ == '__main__':
    with open('freeproxy.txt', 'r') as f:
        rf = f.readlines()
    proxy_list = [ x.strip('\n') for x in rf if x.strip('\n') != '']
    validate_proxt = []

    for p in proxy_list[3566:]:
        proxies = {
            'https': 'http://%s' %(p),
        }
        try:
            r = requests.get('https://www.autodata.com/',
                         proxies=proxies, timeout=5)
        except Exception:
            print('bad ip', p)
            continue

        if r.status_code == requests.codes.ok:
            print('good ip', p)
            validate_proxt.append(p)
            if len(validate_proxt) > 40:
                break


    with open('validate_proxys.txt', 'a') as f:
        json.dump(validate_proxt, f)
