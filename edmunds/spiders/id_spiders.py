# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from edmunds.items import CarItem
from sqlalchemy import Column, Integer, String, create_engine, exc, orm

class IdSpidersSpider(scrapy.Spider):
    name = 'id_spiders'


    def __init__(self):
        pass

    def start_requests(self):
        url = 'https://www.edmunds.com/api-vd/api/vehicle-directory-ajax/findmakes/?fmt=json&pagetype=comparator&ps=new'
        yield scrapy.Request(url, callback=self.parse_make)

    def parse_make(self, response):
        makes = json.loads(response.text)['makes']
        url = 'https://www.edmunds.com/api-vd/api/vehicle-directory-ajax/findmakemodels/?' \
              'fmt=json&yearFormat=expanded&pagetype=comparator&ps=new&excludepreprod&make={}'
        for m in makes:
            m_id = makes[m]['id']
            m_name = makes[m]['name']
            m_link = makes[m]['link']
            m_nicename = makes[m]['niceName']
            m_url = url.format(m_nicename)
            yield scrapy.Request(url=m_url, meta={'make': m_nicename, 'make_id': m_id},
                           callback=self.parse_models)

    def parse_models(self, response):
        models = json.loads(response.text)['models']
        url = 'https://www.edmunds.com/api-vd/api/vehicle-directory-ajax/styles/findmodelyearstyles/?' \
              'make={make}&model={model}&year={year}&sub={sub}&pagetype=comparator&fmt=json&ps=new&excludepreprod'
        for m in models:
            m_id = models[m]['id']
            m_name = models[m]['name']
            m_link = models[m]['link']
            m_submodel = models[m]['submodel']
            m_model = models[m]['model']
            m_modelname = models[m]['modelname']
            m_bodytypes = models[m]['bodytypes']
            m_new_years = models[m]['years']['NEW']
            m_used_years = models[m]['years']['USED'] if hasattr(models[m]['years'], 'USED') else []
            m_years = m_new_years if len(m_new_years)>len(m_used_years) else m_used_years
            for y in m_years:
                m_url = url.format(make=response.meta['make'], model=m_model, year=y, sub=m_submodel)
                yield scrapy.Request(url=m_url,
                                     meta={
                                         'make': response.meta['make'], 'make_id': response.meta['make_id'],
                                         'model_id': m_id, 'model_name': m_name,
                                         'model_submodel': m_submodel, 'yaer': y},
                                     callback=self.parse)

    def parse(self, response):
        item = CarItem()
        styles = json.loads(response.text)['styles']
        for s in styles:
            if isinstance(styles[s], list):
                for i in styles[s]:
                    item['car_name'] = i['styleLongName']
                    item['car_id'] = i['id']
                    item['price'] = i['price']
                    item['trim'] = i['trim']
                    item['submodel'] = response.meta['model_submodel']
                    item['make_name'] = response.meta['make']
                    item['make_id'] = response.meta['make_id']
                    item['model_id'] = response.meta['model_id']
                    item['model_name'] = response.meta['model_name']
                    item['year'] = response.meta['yaer']

                    yield item




