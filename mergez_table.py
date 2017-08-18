# -*- coding:utf-8 -*-
__author__ = "ganbin"
import MySQLdb
import logging

if __name__ == '__main__':

    connect = MySQLdb.connect(user='root', password='', database='automotive')
    cursor = connect.cursor()
    logging.basicConfig(filename='merge.log', level='DEBUG')
    loger = logging.getLogger('autodata')

    cursor.execute('SELECT make, model, year, id FROM automotive.car_styles')
    styles = cursor.fetchall()
    style = {}

    for s in styles:
        try:
            sql = 'UPDATE car_features SET make=%s, model=%s, year=%s WHERE id=%s'
            cursor.execute(sql, s)
            loger.debug(sql % s)
        except:
            connect.rollback()
        finally:
            connect.commit()
        # break
    cursor.close()
    connect.close()
