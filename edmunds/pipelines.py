# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import edmunds.settings as settings
import logging


class EdmundsPipeline(object):
    logger = logging.getLogger(__name__)


    def process_item(self, item, spider):
        if spider.name in ['edmunds_cars_spider',]:
            sql = 'INSERT INTO car_features3(id, make, model, year) VALUES ' \
                  '(%(id)s, %(make)s, %(model)s, %(year)s)'
            self._excute_db(sql, item._values)
            return item

        if spider.name in ['edmunds_cars2_spider',]:
            sql = 'INSERT INTO edmunds_cars(id, make, model, submodel, year) VALUES ' \
                  '(%(id)s, %(make)s, %(model)s, %(submodel)s, %(year)s)'
            self._excute_db(spider.connect, sql, item._values)
            return item

        if spider.name == 'edmunds_feature_spider':
            sql = 'UPDATE edmunds_cars ' \
                  'SET name=%(name)s, baseMsrp=%(baseMsrp)s,msrpWithTypicalOptions=%(msrpWithTypicalOptions)s, ' \
                  'mpg=%(mpg)s, totalSeating=%(totalSeating)s, colors=%(colors)s, ' \
                  'safety=%(safety)s, comfort_convenience=%(comfort_convenience)s, performance=%(performance)s, ' \
                  'technology=%(technology)s, fuel=%(fuel)s, engine=%(engine)s, ' \
                  'measurements=%(measurements)s, frontseats=%(frontseats)s, rearseats=%(rearseats)s, ' \
                  'drive_train=%(drive_train)s, power_feature=%(power_feature)s, instrumentation=%(instrumentation)s, ' \
                  'suspension=%(suspension)s, in_car_entertainment=%(in_car_entertainment)s, warranty=%(warranty)s, ' \
                  'telematics=%(telematics)s, tires_and_wheels=%(tires_and_wheels)s, interior_options=%(interior_options)s, ' \
                  'exterior_options=%(exterior_options)s, packages=%(packages)s' \
                  'WHERE id=%(id)s'
            self._excute_db(spider.connect, sql, item._values)
            return item

        if spider.name == 'firestone_cars_spider':
            sql = 'INSERT INTO firestone_cars(make, model, submodel, year) VALUE ' \
                  '( %(make)s, %(model)s, %(submodel)s, %(year)s)'
            self._excute_db(spider.connect, sql, item._values)
            return item

        if spider.name == 'firestone_tire_spider':
            sql = 'UPDATE firestone_cars SET tire_pressure=%(tire_pressure)s WHERE id=%(id)s'
            self._excute_db(spider.connect, sql, item._values)
            return item

    def _excute_db(self, connect, sql, lis):
        try:
            cursor = connect.cursor()
            cursor.execute(sql, lis)
            self.logger.debug('sql:%s lis:%s' % (sql, lis))
        except Exception as e:
            self.logger.warning(e)
            connect.rollback()
        connect.commit()






