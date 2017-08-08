# -*- coding:utf-8 -*-
__author__ = "ganbin"
import scrapy
import json
from edmunds.items import NewItem

class GetParamsSpider(scrapy.Spider):

    name = 'get_params_spider'


    def __init__(self):
        pass

    def start_requests(self):
        url = 'https://www.edmunds.com'
        yield scrapy.Request(url, callback=self.parse_make)


    def parse_make(self, response):
        make_names = response.xpath('//*[@name="select-make"]/option/@value').extract()
        # print(make_names)
        url = 'https://www.edmunds.com/gateway/api/vehicle/v4/makes/{}/models/'
        for make in make_names[1:]:
            make_url = url.format(make)
            yield scrapy.Request(
                url=make_url,
                meta={'make': make},
                callback=self.parse_model
            )


    def parse_model(self, response):
        url = 'https://www.edmunds.com/gateway/api/vehicle/v4/makes/{}/models/{}/years'
        res_json = json.loads(response.text)
        results = res_json['results']
        make = response.meta['make']
        for model in results:
            model_url = url.format(make, model)
            yield scrapy.Request(
                url=model_url,
                meta={'make': make, 'model': model},
                callback=self.parse_year
            )

    def parse_year(self, response):
        url = 'https://www.edmunds.com/{make}/{model}/{year}/features-specs/'
        res_json = json.loads(response.text)
        results = res_json['results']
        make = response.meta['make']
        model = response.meta['model']
        for submodel in results:
            if results[submodel].get('years'):
                years = results[submodel]['years']
                for year in years:
                    # year_info = years[year] has submodelid yearmodelid , but maybe i don't neet them now
                    year_url = url.format(make=make, model=model, year=year)
                    yield scrapy.Request(
                        url=year_url,
                        meta={
                            'make': make,
                            'model': model,
                            'year': year
                        }
                    )

    def parse(self, response):
        re_style_ids = response.xpath('//*[@class="style-select h5 mb-0 w-100 bg-white font-weight-bold"]/option/@value').extract()
        style_ids = []
        item = NewItem()
        item['make'] = response.meta['make']
        item['model'] = response.meta['model']
        item['year'] = response.meta['year']
        for s in re_style_ids:
            if s in style_ids:
                continue
            style_ids.append(s)
        for style_id in style_ids:
            item['style_id'] = style_id
            # print(item)
            yield item















