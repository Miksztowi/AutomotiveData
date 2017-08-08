# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import pymongo


class EdmundsPipeline(object):
    def __init__(self):
        self.connect = MySQLdb.connect(user='root', password='', db='automotive')
        self.cursor = self.connect.cursor()
        # self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        # self.db = self.client.get_database("car")
        # self.collection = self.db.get_collection("features")

    def open_spider(self, spider):
        if spider.name == 'get_paramas_spider':
            pass # todo use sqlalchemy to realize database options.

    def process_item(self, item, spider):
        if spider.name == 'id_spiders':
            sql = 'INSERT INTO car_informations(' \
                  'car_id, make_id, model_id, make_name, model_name, car_name, year, submodel) ' \
                  'VALUE (%s, %s, %s, %s, %s, %s, %s, %s)'
            lis = (
                item['car_id'], item['make_id'], item['model_id'],
                item['make_name'], item['model_name'], item['car_name'],
                item['year'], item['submodel'])
            self._excute_db(sql, lis)
            return item

        if spider.name == 'configurations_spider':
            sql = 'INSERT INTO car_configurations(' \
                  'car_id, msrp, invoice, true_market_value, base_engine, cylinder, ' \
                  'drive_type, fuel_capacity, fuel_economy, fuel_type, horsepower,' \
                  'monthly_fuel_cost, torque, transmission, ac_with_climate_control,' \
                  'bluetooth, builtin_hard_drive, concierge_service, destination_download,' \
                  'destination_guidance, hd_radio, hand_free_calling, heatedcooled_seats,' \
                  'keyless_ignition, navigation, parking_assistance, power_seats,' \
                  'premium_sound_system, rear_seat_dvd, roadside_assistance, satellite_radio,' \
                  'seating_capacity, upholstery, ipod, all_season_tires, power_glass_sunroof,' \
                  'run_flat_tires, tire_size, wheel_tire_size, wheels, airbag_deployment_notification,' \
                  'anti_lock_brakes, anti_theft_system, child_seat_anchors, emergency_service,' \
                  'side_curtain_airbags, stabillity_control, stolen_vehicle_tracking_assistance,' \
                  'traction_control, vehicle_alarm_notification, average_cost_per_mile,' \
                  'true_cost_to_own, depreciation, taxes_fees, financing, fuel,' \
                  'insurance, maintenance, repairs, tax_credit) ' \
                  'VALUE (   %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            lis = (item['car_id'], item['msrp'], item['invoice'], item['true_market_value'], item['base_engine'], item['cylinder'],
                   item['drive_type'],item['fuel_capacity'], item['fuel_economy'], item['fuel_type'], item['horsepower'],
                   item['monthly_fuel_cost'],item['torque'], item['transmission'], item['ac_with_climate_control'], item['bluetooth'],
                   item['builtin_hard_drive'],item['concierge_service'], item['destination_download'], item['destination_guidance'], item['hd_radio'],
                   item['hand_free_calling'],item['heatedcooled_seats'], item['keyless_ignition'], item['navigation'], item['parking_assistance'],
                   item['power_seats'],item['premium_sound_system'], item['rear_seat_dvd'], item['roadside_assistance'], item['satellite_radio'],
                   item['seating_capacity'],item['upholstery'], item['ipod'], item['all_season_tires'], item['power_glass_sunroof'],
                   item['run_flat_tires'],item['tire_size'], item['wheel_tire_size'], item['wheels'], item['airbag_deployment_notification'],
                   item['anti_lock_brakes'],item['anti_theft_system'], item['child_seat_anchors'], item['emergency_service'], item['side_curtain_airbags'],
                   item['stabillity_control'],item['stolen_vehicle_tracking_assistance'], item['traction_control'], item['vehicle_alarm_notification'], item['average_cost_per_mile'],
                   item['true_cost_to_own'],item['depreciation'], item['taxes_fees'], item['financing'],  item['fuel'], item['insurance'],
                   item['maintenance'], item['repairs'],  item['tax_credit'])
            self._excute_db(sql, lis)
            return item

        if spider.name == 'get_params_spider':
            sql = 'INSERT INTO car_styles VALUES ' \
                  '(%(style_id)s, %(make)s, %(model)s, %(year)s)'
            self._excute_db(sql, item._values)
            return item

        if spider.name == 'features_spider':
            sql = 'INSERT INTO car_features VALUE' \
                  '(%(id)s, %(name)s, %(baseMsrp)s, %(msrpWithTypicalOptions)s, %(mpg)s,'\
                  '%(totalSeating)s, %(colors)s, %(safety)s, %(comfort_convenience)s,' \
                  '%(performance)s, %(technology)s, %(fuel)s, %(engine)s, %(measurements)s, %(frontseats)s,' \
                  '%(rearseats)s, %(drive_train)s, %(power_feature)s, %(instrumentation)s, ' \
                  '%(suspension)s, %(in_car_entertainment)s, %(warranty)s, %(telematics)s, %(tires_and_wheels)s,' \
                  '%(interior_options)s, %(exterior_options)s, %(packages)s)'
            # print(item._values)
            self._excute_db(sql, item._values)
            # return item

    def _excute_db(self, sql, lis):

        self.cursor.execute(sql, lis)

        self.connect.commit()






