from selenium import webdriver
from scrapy import Selector
import scrapy
import MySQLdb
import logging
import re
#
# cookies = {'domain': 'www.firestonecompleteautocare.com',
#   # 'httpOnly': False,
#   'name': 'bsro.cp-fcac',
#   # 'path': '/',
#   # 'secure': False,
#   'value': '%7B%22vehicles%22%3A%7B%22main%22%3A%7B%22lvl%22%3A0%2C%22ymm%22%3A%22%22%2C%22year%22%3A%22%22%2C%22make%22%3A%22%22%2C%22model%22%3A%22%22%2C%22trim%22%3A%22%22%2C%22tpms%22%3A%22%22%2C%22dt%22%3A%22%22%7D%2C%22tce%22%3A%7B%22lvl%22%3A4%2C%22ymm%22%3A%222017-Acura-ILX%22%2C%22year%22%3A%222017%22%2C%22make%22%3A%22Acura%22%2C%22model%22%3A%22ILX%22%2C%22trim%22%3A%22Base%22%2C%22tpms%22%3A%221%22%2C%22dt%22%3A%2208%2F08%2F2017%2003%3A16%3A07%20GMT%22%7D%2C%22aux%22%3A%7B%22lvl%22%3A0%2C%22ymm%22%3A%22%22%2C%22year%22%3A%22%22%2C%22make%22%3A%22%22%2C%22model%22%3A%22%22%2C%22engine%22%3A%22%22%2C%22dt%22%3A%22%22%7D%7D%2C%22site%22%3A%22FCAC%22%2C%22location%22%3A%7B%22storeNumber%22%3A%2212858%22%2C%22locationLvl%22%3A2%2C%22myZip%22%3A%2294301%22%2C%22myCity%22%3A%22%22%2C%22myState%22%3A%22%22%2C%22autoZip%22%3A%2260605%22%7D%2C%22tires%22%3A%7B%22main%22%3A%7B%22lvl%22%3A0%2C%22cs%22%3A%22%22%2C%22ar%22%3A%22%22%2C%22rs%22%3A%22%22%2C%22tireSize%22%3A%22%22%2C%22dt%22%3A%22%22%7D%2C%22tce%22%3A%7B%22lvl%22%3A0%2C%22cs%22%3A%22%22%2C%22ar%22%3A%22%22%2C%22rs%22%3A%22%22%2C%22tireSize%22%3A%22%22%2C%22dt%22%3A%22%22%7D%7D%7D'}
#
# url = 'http://www.firestonecompleteautocare.com/tires/tire-pressure/inflation/'
#
# def parse(response):
#     print(response.text)
#
#
# scrapy.Request(url=url, cookies=cookies, callback=parse)
if __name__ == '__main__':
    logging.basicConfig(filename='intersection.log', level='DEBUG')
    logger = logging.getLogger('inflation_contain2')
    connect = MySQLdb.connect(user='root', password='', database='automotive')
    cursor = connect.cursor()

    # cursor.execute('SELECT make, model, year, b.name, b.id FROM '
    #                 'automotive.car_styles as a INNER JOIN automotive.car_features as b ON a.id=b.id ')
    #
    cursor.execute('SELECT make, model, submodel, year, id FROM automotive.car_styles3')
    fire_car = cursor.fetchall()

    cursor.execute('SELECT make, model, b.name, year, b.id FROM '
                   'automotive.car_styles as a '
                   'INNER JOIN '
                   '(SELECT * FROM automotive.car_features WHERE tire_pressure IS NULL) as b '
                   'ON a.id=b.id')

    edmunds_car = cursor.fetchall()

    fire_car = [[x.lower() if isinstance(x, str) else x for x in a ] for a in fire_car]
    edmunds_car = [[x.lower() if isinstance(x, str) else x for x in a] for a in edmunds_car]
    intersection = []

    for e in edmunds_car:
        e[2] = e[2].split(' ')
        if len(e[2]) < 3:
            e[2] = 'base'
        else:
            e[2] = ''.join(e[2])
        edmunds_index = ''.join(e[:3])
        edmunds_index = re.sub(r'[ -]', '', edmunds_index)
        for f in fire_car:
            fire_index = ''.join(f[:3])
            fire_index = re.sub(r'[ -]', '', fire_index)
            # if edmunds_index in fire_index and e[3]==f[3] and len(edmunds_index)< len(fire_index):
            if ((fire_index in edmunds_index) or (edmunds_index in fire_index)) and f[3]==e[3]:
                intersection.append([e, f])
                logger.debug('%s' % ((e, f),))
                try:
                    cursor.execute('UPDATE car_features SET '
                                   'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                                   'WHERE id=%s' % (f[4], e[4]))
                except Exception as e:
                    connect.rollback()
                    logger.debug('%s' %(e))
                finally:
                    connect.commit()
                break

    cursor.close()
    connect.close()
    print(len(intersection))
