# -*- coding:utf-8 -*-
import scrapy
import json
from edmunds.items import EdmundsItem
import random

class EdmundsCarsSpider(scrapy.Spider):
    name = 'edmunds_cars_spider'
    custom_settings = {
        'CONCURRENT_REQUESTS': 120,
        'DOWNLOAD_DELAY': 0,
    }

    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
            "Connection": "keep-alive",
            "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        }

    def start_requests(self):
        url = 'https://www.edmunds.com'
        yield scrapy.Request(url, headers=self.headers, callback=self.parse_make)

    def parse_make(self, response):
        make_names = response.xpath('//*[@name="select-make"]/option/@value').extract()
        # print(make_names)
        url = 'https://www.edmunds.com/gateway/api/vehicle/v4/makes/{}/models/'
        for make in make_names[1:]:
            make_url = url.format(make)
            yield scrapy.Request(
                url=make_url,
                meta={'make': make},
                headers=self.headers,
                callback=self.parse_model,
                dont_filter=True,
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
                headers=self.headers,
                callback=self.parse_year,
                dont_filter=True,
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
                    # year_info = years[year] have submodelid yearmodelid , but maybe i don't need them now
                    year_url = url.format(make=make, model=model, year=year)
                    yield scrapy.Request(
                        url=year_url,
                        meta={
                            'make': make,
                            'model': model,
                            'year': year
                        },
                        headers = self.headers,
                    )

    def parse(self, response):
        re_style_ids = response.xpath(
            '//*[@class="style-select h5 mb-0 w-100 bg-white font-weight-bold"]/option/@value').extract()
        style_ids = []
        item = EdmundsItem()
        item['make'] = response.meta['make']
        item['model'] = response.meta['model']
        item['year'] = response.meta['year']
        for style_id in re_style_ids:
            if style_id in style_ids:
                continue
            item['id'] = style_id
            style_ids.append(style_id)
            yield item















