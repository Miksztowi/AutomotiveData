# -*- coding:utf-8 -*-
import scrapy
from urllib.parse import quote
from datetime import datetime
import MySQLdb
from autodata.items import StoneItem
import json
import autodata.settings as settings
import logging


class FirestoneTireSpider(scrapy.Spider):
    logger = logging.getLogger(__name__)
    name = 'firestone_feature_spider'
    custom_settings = {
        'CONCURRENT_REQUESTS': 100,
        'DOWNLOAD_DELAY': 0,
        'LOG_FILE': 'firestone_feature.log',
    }

    def __init__(self, *args):
        self.connect = MySQLdb.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            db=settings.DB,
        )
        self.cursor = self.connect.cursor()

    def start_requests(self):
        url = 'http://www.firestonecompleteautocare.com/tires/tire-pressure/inflation/'
        self.cursor.execute(
            'SELECT make, model, submodel, year '
            'FROM firestone_cars WHERE tire_pressure IS NULL'
        )
        cars_param = self.cursor.fetchall()
        map_params = map(self._configuration_params, cars_param)

        for p, primary in map_params:
            param = quote(p)
            cookies = {
                "bsro.cp-fcac": param
            }
            yield scrapy.Request(url=url, cookies=cookies,
                                 callback=self.parse, dont_filter=True,
                                 meta={'primary': primary})

    def parse(self, response):
        item = StoneItem()
        item['make'] = response.meta['primary'][0]
        item['model'] = response.meta['primary'][1]
        item['submodel'] = response.meta['primary'][2]
        item['year'] = response.meta['primary'][3]

        tires_res = response.xpath('//*[@class="results"]/table/tbody')
        tire_configurations = [x.strip('\n ') for x in tires_res.xpath('tr//*/text()').extract()]
        tire_pressure_list = []
        for t in tire_configurations:  # pop data
            item['standard_optional'] = tire_configurations.pop()
            item['rear_inflation'] = tire_configurations.pop()
            item['front_inflation'] = tire_configurations.pop()
            item['speed_rating'] = tire_configurations.pop()
            item['size'] = tire_configurations.pop()
            item['front_rear_both'] = tire_configurations.pop()
            tire_pressure = {
                "standard_optional": item['standard_optional'],
                "rear_inflation": item['rear_inflation'],
                "front_inflation": item['front_inflation'],
                "speed_rating": item['speed_rating'],
                "size": item['size'],
                "front_rear_both": item['front_rear_both'],
            }
            tire_pressure_list.append(tire_pressure)
        item['tire_pressure'] = json.dumps(tire_pressure_list)
        return item

    def _configuration_params(self, configurations):
        _make, _model, _submodel, _year = (x for x in range(4))
        ymm = "%s-%s-%s" % (configurations[_year], configurations[_make], configurations[_model])
        year = configurations[_year]
        make = configurations[_make]
        model = configurations[_model]
        trim = configurations[_submodel]
        convert2gmt = lambda a: a.strftime("%d/%m/%Y %H:%M:%S") + " GMT"
        dt = convert2gmt(datetime.utcnow())  # 08/08/2017 02:50:36 GMT
        base = '{"vehicles":{"main":{"lvl":0,"ymm":"","year":"","make":"","model":"","trim":"","tpms":"","dt":""},' \
               '"tce":{"lvl":4,"ymm": "%s","year": "%s","make": "%s","model":"%s","trim":"%s",' \
               '"tpms":"0","dt":"%s"},' \
               '"aux":{"lvl":0,"ymm":"","year":"","make":"","model":"","engine":"","dt":""}},' \
               '"site":"FCAC",' \
               '"location":{"storeNumber":"12858","locationLvl":2,"myZip":"94301",' \
               '"myCity":"","myState":"","autoZip":"60605"},' \
               '"tires":{"main":{"lvl":0,"cs":"","ar":"","rs":"","tireSize":"","dt":""},' \
               '"tce":{"lvl":0,"cs":"","ar":"","rs":"","tireSize":"","dt":""}}}'
        vehicles = base % (ymm, year, make, model, trim, dt)
        return vehicles, (make, model, trim, year)

    def spider_closed(self, spider):
        self.cursor.close()
        self.connect.close()
        spider.logger.info('Spider closed: %s', spider.name)
