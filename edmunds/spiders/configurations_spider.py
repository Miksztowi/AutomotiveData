# -*- coding:utf-8 -*-
import scrapy
import csv
import MySQLdb
from edmunds.items import CarItem

class ConfigurationsSpider(scrapy.Spider):
    name = 'configurations_spider'

    def __init__(self, *args):
        self.connect = MySQLdb.connect(user='root', password='', db='automotive')
        self.cursor = self.connect.cursor()

    def start_requests(self):

        flag = 0  # 控制一次查询的car id数量
        car_params = []
        car_ids = []
        base_url = 'https://www.edmunds.com/car-comparisons/?' \
                   'veh1={0[0]}&' \
                   'veh2={0[1]}&' \
                   'veh3={0[2]}&' \
                   'veh4={0[3]}&' \
                   'show=0' \
                   # '&comparatorId=653347'
        self.cursor.execute('SELECT car_id FROM car_informations')
        new_cars = self.cursor.fetchall()

        self.cursor.execute('SELECT car_id FROM car_configurations')
        old_cars = self.cursor.fetchall()
        cars_id = list(set([x[0] for x in new_cars]).difference(set([x[0] for x in old_cars])))

        cars_ids = ','.join(cars_id)
        print(car_ids)
        if car_ids:
            self.cursor.execute('SELECT car_id, submodel FROM car_informations where car_id in (%s)' % cars_ids)
            cars = self.cursor.fetchall()
        else:
            cars = []

        pad_times = 4 - (len(cars) % 4)
        times = len(cars) // 4
        count = 0
        for c in cars:
            param = '%s|%s' % (c[0], c[1])
            car_params.append(param)
            car_ids.append(c[0])
            flag += 1
            if flag == 4:
                url = base_url.format(car_params)
                yield scrapy.Request(url=url, meta={'cars_id': car_ids})
                car_params = []
                car_ids = []
                flag = 0
                count += 1
                if count == times:
                    for i in range(pad_times):
                        car_params.append(param)
                        car_ids.append(c[0])



    def parse(self, response):
        item = CarItem()
        cars = {}
        vehicle = response.xpath('//*[@id="vehicle-compare"]/div')
        cars['car_id'] = response.meta['cars_id']

        # pricing summary
        large_list = response.xpath('//*[@class="row large"]/div/text()').extract()
        cars['msrp'] = [l.strip('\n ') for l in large_list[1:5]]
        cars['invoice'] = [l.strip('\n ') for l in large_list[6:10]]
        cars['true_market_value'] = [l.strip('\n ') for l in large_list[11:21:3]]

        # mechanical
        mechanical = {}
        mechanicals = vehicle[2].xpath('div/div/div')
        features = [x.strip('\n ') for x in mechanicals.xpath('div/text()').extract()]
        for i in range(0,len(features)):
            try:
                if features[i] == '' and features[i] == features[i-1]:
                    features.pop(i)
            except:
                continue
        cars['base_engine'] = features[0:4]
        cars['cylinder'] = features[4:8]
        cars['drive_type'] = features[8:12]
        cars['fuel_capacity'] = features[12:16]
        cars['fuel_economy'] = features[16:20]
        cars['fuel_type'] = features[20:24]
        cars['horsepower'] = features[24:28]
        cars['monthly_fuel_cost'] = features[28:32]
        cars['torque'] = features[32:36]
        cars['transmission'] = features[36:40]

        # interior
        interior = {}
        interiors = vehicle[3].xpath('div/div/div')
        features = [x.strip('\n ') for x in interiors.xpath('div[@class="cell"]/text()').extract()]
        for i in range(0,len(features)):
            try:
                if features[i] == '' and features[i] == features[i-1]:
                    features.pop(i)
            except:
                continue
        cars['ac_with_climate_control'] = features[0:4]
        cars['bluetooth'] = features[4:8]
        cars['builtin_hard_drive'] = features[8:12]
        cars['concierge_service'] = features[12:16]
        cars['destination_download'] = features[16:20]
        cars['destination_guidance'] = features[20:24]
        cars['hd_radio'] = features[24:28]
        cars['hand_free_calling'] = features[28:32]
        cars['heatedcooled_seats'] = features[32:36]
        cars['keyless_ignition'] = features[36:40]
        cars['navigation'] = features[40:44]
        cars['parking_assistance'] = features[44:48]
        cars['power_seats'] = features[48:52]
        cars['premium_sound_system'] = features[52:56]
        cars['rear_seat_dvd'] = features[56:60]
        cars['roadside_assistance'] = features[60:64]
        cars['satellite_radio'] = features[64:68]
        cars['seating_capacity'] = features[68:72]
        cars['upholstery'] = features[72:76]
        cars['ipod'] = features[76:80]

        # exterior
        exterior = {}
        exteriors = vehicle[4].xpath('div/div/div')
        features = [x.strip('\n ') for x in exteriors.xpath('div[@class="cell"]/text()').extract()]
        for i in range(0,len(features)):
            try:
                if features[i] == '' and features[i] == features[i-1]:
                    features.pop(i)
            except:
                continue
        cars['all_season_tires'] = features[0:4]
        cars['power_glass_sunroof'] = features[4:8]
        cars['run_flat_tires'] = features[8:12]
        cars['tire_size'] = features[12:16]
        cars['wheel_tire_size'] = features[16:20]
        cars['wheels'] = features[20:24]

        # safety
        safety = {}
        safetys = vehicle[5].xpath('div/div/div')
        features = [x.strip('\n ') for x in safetys.xpath('div[@class="cell"]/text()').extract()]
        for i in range(0,len(features)):
            try:
                if features[i] == '' and features[i] == features[i-1]:
                    features.pop(i)
            except:
                continue
        cars['airbag_deployment_notification'] = features[0:4]
        cars['anti_lock_brakes'] = features[4:8]
        cars['anti_theft_system'] = features[8:12]
        cars['child_seat_anchors'] = features[12:16]
        cars['emergency_service'] = features[16:20]
        cars['side_curtain_airbags'] = features[20:24]
        cars['stabillity_control'] = features[24:28]
        cars['stolen_vehicle_tracking_assistance'] = features[28:32]
        cars['traction_control'] = features[32:36]
        cars['vehicle_alarm_notification'] = features[36:40]


        # 5-year ownership cost
        cost = {}
        costs = vehicle[9].xpath('div/div/div')
        features = [x.strip('\n ') for x in costs.xpath('div[@class="cell"]/text()').extract()]
        for i in range(0,len(features)):
            try:
                if features[i] == '' and features[i] == features[i-1]:
                    features.pop(i)
            except:
                continue
        cars['average_cost_per_mile'] = features[0:4]
        cars['true_cost_to_own'] = features[4:8]
        cars['depreciation'] = features[8:12]
        cars['taxes_fees'] = features[12:16]
        cars['financing'] = features[16:20]
        cars['fuel'] = features[20:24]
        cars['insurance'] = features[24:28]
        cars['maintenance'] = features[28:32]
        cars['repairs'] = features[32:36]
        cars['tax_credit'] = features[36:40]

        for i in range(0,4):
            for c in cars:
                try:
                    item[c] = cars[c][i]

                except:
                    print(cars[c])
            print(type(item))
            print(dir(item))
            return item


