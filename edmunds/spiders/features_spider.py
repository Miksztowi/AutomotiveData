# -*- coding:utf-8 -*-
__author__ = "ganbin"
import scrapy
import MySQLdb
import json
from edmunds.items import  NewItem

class FeaturesSpider(scrapy.Spider):
    name = 'features_spider'

    def __init__(self):
        self.connect = MySQLdb.connect(user='root', password='', db='automotive')
        self.cursor = self.connect.cursor()  # todo  how to aovid this options?

    def start_requests(self):
        self.cursor.execute('SELECT style_id FROM car_styles')
        new_cars = {x[0] for x in self.cursor.fetchall()}

        self.cursor.execute('SELECT id FROM car_features')
        old_cars = {x[0] for x in self.cursor.fetchall()}

        style_ids = list(new_cars.difference(old_cars))
        base_url = 'https://www.edmunds.com/api/groundwork/feature/styles?styleIds={}'
        for style_id in style_ids:
            url = base_url.format(style_id)
            yield scrapy.Request(
                url=url,
                meta={'style_id': style_id}
            )

    def parse(self, response):
        res_json = json.loads(response.text)
        item = NewItem()
        if res_json.get('styles'):
            styles = res_json.pop('styles')[0] # list
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



