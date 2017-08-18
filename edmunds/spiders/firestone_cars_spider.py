# -*- coding:utf-8 -*-
import scrapy
import json
from edmunds.items import StoneItem
from urllib.parse import quote
import MySQLdb
import edmunds.settings as settings
import logging


class FirestoneCarsSpider(scrapy.Spider):
    name = 'firestone_cars_spider'
    custom_settings = {
        'CONCURRENT_REQUESTS': 50,
        'DOWNLOAD_DELAY': 0,
        'LOG_FILE': 'firestone_cars.log',
    }
    logger = logging.getLogger(__name__)


    def __init__(self):
        self.connect = MySQLdb.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB
        )
        self.cursor = self.connect.cursor()

    #  get years
    def start_requests(self):
        url = 'http://www.firestonecompleteautocare.com/bsro/services/vehicle/get-years?vehicleType=tce'
        yield scrapy.Request(url=url, callback=self.get_makes)

    def get_makes(self, response):
        base_url = 'http://www.firestonecompleteautocare.com/bsro/services/vehicle/get-makes?year={}&vehicleType=tce'
        res_json = json.loads(response.text)
        year_list = res_json['data']['year']
        year_generator = self._generate_url(base_url, year_list)
        for url, year in year_generator:
            yield scrapy.Request(url=url, callback=self.get_models,
                                 meta={'year': year})

    def get_models(self, response):
        base_url = 'http://www.firestonecompleteautocare.com/bsro/services/vehicle/get-models?' \
                   'make={}&year={}&vehicleType=tce'
        res_json = json.loads(response.text)
        make_list = res_json['data']['makes']
        make_generator = self._generate_url(base_url, make_list, response.meta['year'])
        for url, make in make_generator:
            yield scrapy.Request(url=url, callback=self.get_submodels,
                                 meta={'year': response.meta['year'], 'make': make})

    def get_submodels(self, response):
        base_url = 'http://www.firestonecompleteautocare.com/bsro/services/vehicle/get-trims?' \
                   'model={}&year={}&make={}&vehicleType=tce'
        res_json = json.loads(response.text)
        model_list = res_json['data']['models']
        model_generator = self._generate_url(base_url, model_list,
                                             response.meta['year'], response.meta['make'])
        for url, model in model_generator:
            yield scrapy.Request(url=url, callback=self.parse,
                                  meta={'year': response.meta['year'],
                                        'make': response.meta['make'], 'model': model})

    def parse(self, response):
        item = StoneItem()
        item['year'] = response.meta['year']
        item['make'] = response.meta['make']
        item['model'] = response.meta['model']
        res_json = json.loads(response.text)
        trim_list = res_json['data']['trims']
        for t in trim_list:
            item['submodel'] = t['trim']
            yield item

    # avoid getting quoted data and 502 error_code
    def _generate_url(self,base_url, *args):
        if len(args) > 1:
            index_param, *other_params = args
            quoted_args = [quote(x) for x in other_params]
        else:
            index_param = args[0]
            quoted_args = []
        for p in index_param:
            quoted_p = quote(p)
            yield (base_url.format(quoted_p, *quoted_args), p)

    def spider_closed(self, spider):
        self.cursor.close()
        self.connect.close()
        self.connect.close()
        spider.logger.info('Spider closed: %s', spider.name)


