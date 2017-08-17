# -*- coding:utf-8 -*-
__author__ = "ganbin"
import scrapy
import json
from edmunds.items import StoneItem

class FireStone(scrapy.Spider):
    name = 'firestone_spider'

    def __init__(self):
        pass

    #  get years
    def start_requests(self):
        url = 'http://www.firestonecompleteautocare.com/bsro/services/vehicle/get-years?vehicleType=tce'
        yield scrapy.Request(url=url, callback=self.get_makes)

    def get_makes(self, response):
        base_url = 'http://www.firestonecompleteautocare.com/bsro/services/vehicle/get-makes?year={}&vehicleType=tce'
        res_json = json.loads(response.text)
        year_list = res_json['data']['year']
        year_generator = self._generate_url(base_url=base_url, param_list=year_list)
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

    def _generate_url(self,base_url, param_list, *args):
        for p in param_list:
            yield (base_url.format(p, *args), p)


