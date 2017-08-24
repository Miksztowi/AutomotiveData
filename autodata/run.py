# -*- coding:utf-8 -*-
import optparse
import MySQLdb
import merge
import subprocess
import proxy_pool
import settings



def main():
    options = optparse.OptionParser(
        usage='-m <Mysql Url> [-s <Spider Name>] [--merge <Merge data tables>]',
                                    description="Auto's data"
    )
    options.add_option('-s', '--spider', type='string', dest='spider',
                       action='callback', callback=_run_spider,
                       help='Run spider                                                          '
                            '<-s edmunds_car/edmunds_feature/firstone_car/firestone_feature>'
                            '                                       Default choose all spider')
    options.add_option('--merge', action='callback',
                       callback=_merge, help="Merge Car's Tables")

    options.add_option('--proxy', action='callback',
                       callback=_validate_proxy, help="Update new proxies")
    options.add_option('--mysql',  dest='mysql',
                       action='callback', callback=_create_table, help='Create Mysql DataBase and Tables')

    opts, args = options.parse_args()


def _create_table(option, opt_str, value, parser):
    CREATE_TABLES_SQL = {
        "autodata": "CREATE TABLE `edmunds_cars` (`id` int(11) NOT NULL,`make` varchar(200) DEFAULT NULL,`model` varchar(200) DEFAULT NULL,`submodel` varchar(200) DEFAULT NULL,`name` varchar(200) DEFAULT NULL, `year` varchar(100) DEFAULT NULL,`baseMsrp` varchar(45) DEFAULT NULL, `msrpWithTypicalOptions` varchar(45) DEFAULT NULL,`mpg` varchar(45) DEFAULT NULL, `totalSeating` varchar(45) DEFAULT NULL,`colors` json DEFAULT NULL, `safety` json DEFAULT NULL,`comfort_convenience` json DEFAULT NULL,`performance` json DEFAULT NULL,`technology` json DEFAULT NULL,`fuel` json DEFAULT NULL,`engine` json DEFAULT NULL,`measurements` json DEFAULT NULL,`frontseats` json DEFAULT NULL,`rearseats` json DEFAULT NULL, `drive_train` json DEFAULT NULL,`power_feature` json DEFAULT NULL,`instrumentation` json DEFAULT NULL,`suspension` json DEFAULT NULL,`in_car_entertainment` json DEFAULT NULL,`warranty` json DEFAULT NULL,`telematics` json DEFAULT NULL,`tires_and_wheels` json DEFAULT NULL,`interior_options` json DEFAULT NULL,`exterior_options` json DEFAULT NULL,`packages` json DEFAULT NULL,`tire_pressure` json DEFAULT NULL,PRIMARY KEY (`id`), UNIQUE KEY `id_UNIQUE` (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8",
        "firestone": 'CREATE TABLE `firestone_cars` (`make` varchar(200) NOT NULL,`model` varchar(200) NOT NULL,`submodel` varchar(200) NOT NULL,`year` varchar(200) NOT NULL,`tire_pressure` json DEFAULT NULL, PRIMARY KEY (`model`,`make`,`submodel`,`year`)) ENGINE=InnoDB DEFAULT CHARSET=utf8',
    }
    connect, cursor = _connect_db()
    try:
        cursor.execute(CREATE_TABLES_SQL['autodata'])
        cursor.execute(CREATE_TABLES_SQL['firestone'])
    except MySQLdb.OperationalError:
        connect.rollback()
        raise
    finally:
        cursor.close()
        connect.close()


def _connect_db():
    CREATE_DB_SQL = {
        'automotive': "CREATE DATABASE automotive"
    }
    try:
        _connect = MySQLdb.connect(
            host=settings.DB_HOST, port=settings.DB_PORT,
            user=settings.DB_USER, password=settings.DB_PASSWORD
        )
        _cursor = _connect.cursor()
        _cursor.execute(CREATE_DB_SQL['automotive'])
        _connect.commit()
    except MySQLdb.DatabaseError:
        _connect.rollback()
    except MySQLdb.OperationalError:
        raise
    finally:
        connect = MySQLdb.connect(
            host=settings.DB_HOST, port=settings.DB_PORT,
            user=settings.DB_USER, password=settings.DB_PASSWORD, database=settings.DB
        )
    cursor = connect.cursor()
    return connect, cursor


def _merge(option, opt_str, value, parser):
    try:
        merge.merge()
    except KeyboardInterrupt:
        print("\n[I] Shutting down...")


def _run_spider(option, opt_str, value, parser):
    RUN_SPIDER = {
        'edmunds_car': 'Scrapy crawl edmunds_cars_spider',
        'edmunds_feature': 'Scrapy crawl edmunds_feature_spider',
        'firestone_car': 'Scrapy crawl firestone_cars_spider',
        'firestone_feature': 'Scrapy crawl firestone_feature_spider',
    }
    if RUN_SPIDER.get(value):
        try:
            subprocess.call(RUN_SPIDER[value], shell=True)
        except KeyboardInterrupt:
            print("\n[I] Shutting down...")
    else:
        print('params error')
        print('Usage: -s edmunds_car/edmunds_feature/firestone_car/firestone_feature')


def _validate_proxy(option, opt_str, value, parser):
    try:
        proxy = proxy_pool.ProxyPool()
        proxy.validate_proxies()
    except KeyboardInterrupt:
        print("\n[I] Shutting down...")

if __name__ == '__main__':
    main()
