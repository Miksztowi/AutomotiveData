# -*- coding:utf-8 -*-
import scrapy
import MySQLdb
import json
from autodata.items import EdmundsItem
import logging
import autodata.settings as settings



class EdmundsFeatureSpider(scrapy.Spider):
    logger  = logging.getLogger(__name__)
    name = 'edmunds_feature_spider'
    custom_settings = {
        'CONCURRENT_REQUESTS': 100,
        'DOWNLOAD_DELAY': 0,
        'LOG_FILE': 'edmunds_feature.log'
    }

    def __init__(self):
        self.connect = MySQLdb.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB
        )
        self.cursor = self.connect.cursor()

    def start_requests(self):
        self.cursor.execute('SELECT id FROM edmunds_cars WHERE name IS NULL')
        style_ids = [x[0] for x in self.cursor.fetchall()]

        base_url = 'https://www.autodata.com/api/groundwork/feature/styles?styleIds={}'
        for style_id in style_ids:
            url = base_url.format(style_id)
            yield scrapy.Request(
                url=url,
                meta={'style_id': style_id}
            )

    def parse(self, response):
        res_json = json.loads(response.text)
        item = EdmundsItem()
        if res_json.get('styles'):
            styles = res_json.pop('styles')[0]  # list
            features = styles['features']
            item['name'] = styles['name']
            item['id'] = styles['id']
            item['baseMsrp'] = styles['baseMsrp']
            item['msrpWithTypicalOptions'] = styles['msrpWithTypicalOptions']
            item['mpg'] = styles['mpg']
            item['totalSeating'] = styles['totalSeating']
            item['colors'] = json.dumps(styles['colors'])
            item['safety'] = json.dumps(features['Safety'])
            item['comfort_convenience'] = json.dumps(features['Comfort & Convenience'])
            item['performance'] = json.dumps(features['Performance'])
            item['technology'] = json.dumps(features['Technology'])
            item['fuel'] = json.dumps(features['Fuel'])
            item['engine'] = json.dumps(features['Engine'])
            item['measurements'] = json.dumps(features['Measurements'])
            item['frontseats'] = json.dumps(features['Frontseats'])
            item['rearseats'] = json.dumps(features['Rearseats'])
            item['drive_train'] = json.dumps(features['Drive Train'])
            item['power_feature'] = json.dumps(features['Power Feature'])
            item['instrumentation'] = json.dumps(features['Instrumentation'])
            item['suspension'] = json.dumps(features['Suspension'])
            item['in_car_entertainment'] = json.dumps(features['In Car Entertainment'])
            item['warranty'] = json.dumps(features['Warranty'])
            item['telematics'] = json.dumps(features['Telematics'])
            item['tires_and_wheels'] = json.dumps(features['Tires and Wheels'])
            item['interior_options'] = json.dumps(features['Interior Options'])
            item['exterior_options'] = json.dumps(features['Exterior Options'])
            item['packages'] = json.dumps(features['Packages'])
        return item

    def spider_closed(self, spider):
        self.cursor.close()
        self.connect.close()
        self.connect.close()
        spider.logger.info('Spider closed: %s', spider.name)



