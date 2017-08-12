from selenium import webdriver
from scrapy import Selector
import scrapy
import MySQLdb
import logging
import re

def direct_merge():
        for e in edmunds_lower:
            e[2] = e[2].split(' ')[0]
            edmunds_index = ''.join(e[:4])
            if edmunds_index not in edmunds_dict:
                edmunds_dict[edmunds_index] = e[4]
        for f in fire_lower:
            fire_index = ''.join(f[:4])
            if fire_index not in fire_dict:
                fire_dict[fire_index] = (f[4], f[5])

        for e_key in edmunds_dict:
            if e_key in fire_dict:
                e_id = edmunds_dict[e_key]
                f_id = fire_dict[e_key][0]
                flag = fire_dict[e_key][1]
                flag += 1
                try:
                    results.append((e_id,e_key))
                    cursor.execute('UPDATE car_features SET '
                                   'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                                   'WHERE id=%s' % (f_id, e_id))
                    cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' %(flag, f_id))
                    logger.debug('%s has update' %((e_key, e_id, f_id),))
                except Exception as e:
                    connect.rollback()
                    logger.debug('%s' %(e))
                finally:
                    connect.commit()
        print(len(results))

def base_merge():
    for e in edmunds_lower:
        e[2] = e[2].split(' ')
        if len(e[2]) < 3:
            e[2] = 'base'
        else:
            continue
        edmunds_index = ''.join(e[:4])
        if edmunds_index not in edmunds_dict:
            edmunds_dict[edmunds_index] = e[4]
    for f in fire_lower:
        fire_index = ''.join(f[:4])
        if fire_index not in fire_dict:
            fire_dict[fire_index] = (f[4], f[5])

    for e_key in edmunds_dict:
        if e_key in fire_dict:
            e_id = edmunds_dict[e_key]
            f_id = fire_dict[e_key][0]
            flag = fire_dict[e_key][1]
            flag += 1
            try:
                results.append((e_id, e_key))
                cursor.execute('UPDATE car_features SET '
                               'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                               'WHERE id=%s' % (f_id, e_id))
                cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' % (flag, f_id))
                logger.debug('%s has update' % ((e_key, e_id, f_id),))
            except Exception as e:
                connect.rollback()
                logger.debug('%s' % (e))
            finally:
                connect.commit()
    print(len(results))

def re_merge():
    for e in edmunds_lower:
        e[2] = e[2].split(' ')
        if len(e[2]) < 3:
            e[2] = 'base'
        else:
            e[2] = e[2][0]
        edmunds_index = ''.join(e[:4])
        edmunds_index = re.sub(r'[ -]', '', edmunds_index)
        if edmunds_index not in edmunds_dict:
            edmunds_dict[edmunds_index] = e[4]
    for f in fire_lower:
        fire_index = ''.join(f[:4])
        fire_index = re.sub(r'[ -]', '', fire_index)
        if fire_index not in fire_dict:
            fire_dict[fire_index] = (f[4], f[5])

    for e_key in edmunds_dict:
        if e_key in fire_dict:
            e_id = edmunds_dict[e_key]
            f_id = fire_dict[e_key][0]
            flag = fire_dict[e_key][1]
            flag += 1
            try:
                results.append((e_id, e_key))
                cursor.execute('UPDATE car_features SET '
                               'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                               'WHERE id=%s' % (f_id, e_id))
                cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' % (flag, f_id))
                logger.debug('%s has update' % ((e_key, e_id, f_id),))
            except Exception as e:
                connect.rollback()
                logger.debug('%s' % (e))
            finally:
                connect.commit()
    print(len(results))

def base_re_merge():
    for e in edmunds_lower:
        e[2] = e[2].split(' ')
        if 'dr' in e[2][0]:
            e[2] = 'base'
        else:
            continue
        edmunds_index = ''.join(e[:4])
        edmunds_index = re.sub(r'[ -]', '', edmunds_index)
        if edmunds_index not in edmunds_dict:
            edmunds_dict[edmunds_index] = e[4]
    for f in fire_lower:
        fire_index = ''.join(f[:4])
        fire_index = re.sub(r'[ -]', '', fire_index)
        if fire_index not in fire_dict:
            fire_dict[fire_index] = (f[4], f[5])

    for e_key in edmunds_dict:
        if e_key in fire_dict:
            e_id = edmunds_dict[e_key]
            f_id = fire_dict[e_key][0]
            flag = fire_dict[e_key][1]
            flag += 1
            try:
                results.append((e_id, e_key))
                cursor.execute('UPDATE car_features SET '
                               'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                               'WHERE id=%s' % (f_id, e_id))
                cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' % (flag, f_id))
                logger.debug('%s has update' % ((e_key, e_id, f_id),))
            except Exception as e:
                connect.rollback()
                logger.debug('%s' % (e))
            finally:
                connect.commit()
    print(len(results))

def submodel_model_merge():
    for e in edmunds_lower:
        e[2] = e[2].split(' ')
        if 'dr' in e[2][0]:
            e[2] = 'base'
        else:
            e[2] = e[2][0]
        edmunds_index = ''.join([e[i] for i in [0, 2, 3]])
        edmunds_index = re.sub(r'[ -]', '', edmunds_index)
        if edmunds_index not in edmunds_dict:
            edmunds_dict[edmunds_index] = e[4]
    for f in fire_lower:
        fire_index = ''.join([f[i] for i in [0, 1, 3]])
        fire_index = re.sub(r'[ -]', '', fire_index)
        if fire_index not in fire_dict:
            fire_dict[fire_index] = (f[4], f[5])

    for e_key in edmunds_dict:
        if e_key in fire_dict:
            e_id = edmunds_dict[e_key]
            f_id = fire_dict[e_key][0]
            flag = fire_dict[e_key][1]
            flag += 1
            try:
                continue
                results.append((e_id, e_key))
                cursor.execute('UPDATE car_features SET '
                               'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                               'WHERE id=%s' % (f_id, e_id))
                cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' % (flag, f_id))
                logger.debug('%s has update' % ((e_key, e_id, f_id),))
            except Exception as e:
                connect.rollback()
                logger.debug('%s' % (e))
            finally:
                connect.commit()
    print(len(results))

def model_submodel_merge():
    for e in edmunds_lower:
        e[2] = e[2].split(' ')
        if 'dr' in e[2][0]:
            e[2] = 'base'
        else:
            e[2] = e[2][0]
        edmunds_index = ''.join([e[i] for i in [0, 1, 3]])
        edmunds_index = re.sub(r'[ -]', '', edmunds_index)
        if edmunds_index not in edmunds_dict:
            edmunds_dict[edmunds_index] = e[4]
    for f in fire_lower:
        fire_index = ''.join([f[i] for i in [0, 2, 3]])
        fire_index = re.sub(r'[ -]', '', fire_index)
        if fire_index not in fire_dict:
            fire_dict[fire_index] = (f[4], f[5])

    for e_key in edmunds_dict:
        if e_key in fire_dict:
            e_id = edmunds_dict[e_key]
            f_id = fire_dict[e_key][0]
            flag = fire_dict[e_key][1]
            flag += 1
            try:
                continue
                results.append((e_id, e_key))
                cursor.execute('UPDATE car_features SET '
                               'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                               'WHERE id=%s' % (f_id, e_id))
                cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' % (flag, f_id))
                logger.debug('%s has update' % ((e_key, e_id, f_id),))
            except Exception as e:
                connect.rollback()
                logger.debug('%s' % (e))
            finally:
                connect.commit()
    print(len(results))

def name_divide_merge():
    for e in edmunds_lower:
        e[2] = e[2].split(' ')
        if 'dr' in e[2][0]:
            e[2] = 'base'
        else:
            try:
                e[2] = e[2]['++++']
            except:
                continue
        edmunds_index = ''.join([e[i] for i in range(4)])
        edmunds_index = re.sub(r'[ -]', '', edmunds_index)
        if edmunds_index not in edmunds_dict:
            edmunds_dict[edmunds_index] = e[4]
    for f in fire_lower:
        fire_index = ''.join([f[i] for i in range(4)])
        fire_index = re.sub(r'[ -]', '', fire_index)
        if fire_index not in fire_dict:
            fire_dict[fire_index] = (f[4], f[5])

    for e_key in edmunds_dict:
        if e_key in fire_dict:
            e_id = edmunds_dict[e_key]
            f_id = fire_dict[e_key][0]
            flag = fire_dict[e_key][1]
            flag += 1
            try:
                results.append((e_id, e_key))
                cursor.execute('UPDATE car_features SET '
                               'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                               'WHERE id=%s' % (f_id, e_id))
                cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' % (flag, f_id))
                logger.debug('%s has update' % ((e_key, e_id, f_id),))
            except Exception as e:
                connect.rollback()
                logger.debug('%s' % (e))
            finally:
                connect.commit()
    print(len(results))

def all_no_use_submodel():
    for e in edmunds_lower:
        e[2] = e[2].split(' ')
        if 'dr' in e[2][0]:
            e[2] = 'base'
        else:
            try:
                e[2] = e[2][0]
            except:
                continue
        edmunds_index = ''.join([e[i] for i in [0, 1, 3, ]])
        edmunds_index = re.sub(r'[ -]', '', edmunds_index)
        if edmunds_index not in edmunds_dict:
            edmunds_dict[edmunds_index] = e[4]
    for f in fire_lower:
        fire_index = ''.join([f[i] for i in [0, 1, 3]])
        fire_index = re.sub(r'[ -]', '', fire_index)
        if fire_index not in fire_dict:
            fire_dict[fire_index] = (f[4], f[5])
    for e_key in edmunds_dict:
        if e_key in fire_dict:
            e_id = edmunds_dict[e_key]
            f_id = fire_dict[e_key][0]
            flag = fire_dict[e_key][1]
            flag += 1
            try:
                print(e_key)
                continue
                results.append((e_id, e_key))
                cursor.execute('UPDATE car_features SET '
                               'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                               'WHERE id=%s' % (f_id, e_id))
                cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' % (flag, f_id))
                logger.debug('%s has update' % ((e_key, e_id, f_id),))
            except Exception as e:
                connect.rollback()
                logger.debug('%s' % (e))
            finally:
                connect.commit()
    print(len(results))

def each_in():
    for e in edmunds_lower:
        e[2] = e[2].split(' ')
        if 'dr' in e[2][0]:
            e[2] = 'base'
        else:
            try:
                e[2] = e[2][1]
            except:
                continue
        edmunds_index = ''.join([e[i] for i in [0, 1, 2, 3]])
        edmunds_index = re.sub(r'[ -]', '', edmunds_index)
        if edmunds_index not in edmunds_dict:
            edmunds_dict[edmunds_index] = e[4]
    for f in fire_lower:
        fire_index = ''.join([f[i] for i in [0, 1, 3]])
        fire_index = re.sub(r'[ -]', '', fire_index)
        if fire_index not in fire_dict:
            fire_dict[fire_index] = (f[4], f[5])

    for e_key in edmunds_dict:
        for f_key in fire_dict:
            if (e_key in f_key) or (f_key in e_key):
                e_id = edmunds_dict[e_key]
                f_id = fire_dict[f_key][0]
                flag = fire_dict[f_key][1]
                flag += 1
                try:
                    print(e_key)
                    results.append((e_id, e_key))
                    continue
                    cursor.execute('UPDATE car_features SET '
                                   'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                                   'WHERE id=%s' % (f_id, e_id))
                    cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' % (flag, f_id))
                    logger.debug('%s has update' % ((e_key, e_id, f_id),))
                except Exception as e:
                    connect.rollback()
                    logger.debug('%s' % (e))
                finally:
                    connect.commit()
    print(len(results))


if __name__ == '__main__':
    logging.basicConfig(filename='intersection17.log', level='DEBUG')
    logger = logging.getLogger('filter_suburban_merge')
    connect = MySQLdb.connect(user='root', password='', database='automotive')
    cursor = connect.cursor()

    # cursor.execute('SELECT make, model, year, b.name, b.id FROM '
    #                 'automotive.car_styles as a INNER JOIN automotive.car_features as b ON a.id=b.id ')
    #
    results = [1]

    while results != []:
        results = []
        cursor.execute('SELECT make, model, submodel, year, id, flag FROM automotive.car_styles3')
        fire_car = cursor.fetchall()
        cursor.execute('SELECT make, model, b.name, year, b.id FROM '
                       'automotive.car_styles as a '
                       'INNER JOIN '
                       '(SELECT * FROM automotive.car_features WHERE tire_pressure IS NULL) as b '
                       'ON a.id=b.id')
        edmunds_car = cursor.fetchall()
        fire_lower = [[x.lower() if isinstance(x, str) else x for x in a] for a in fire_car]
        edmunds_lower = [[x.lower() if isinstance(x, str) else x for x in a] for a in edmunds_car]
        edmunds_dict = {}
        fire_dict = {}

        for e in edmunds_lower:
            e[2] = e[2].split(' ')
            # try:
            #     if 'dr' in e[2][0]:
            #         e[2][0] = 'base'
            #     else:
            #         e[2] = e[2][0]
            # except:
            #     continue
            # e[2] = 'base'
            try:
                # if 'dr' not in e[2][1]:
                #     e[1] = e[1] + e[2][1]
                # if e[2][0] == 'gts':
                #     e[2] = 'gtsportback'
                # elif e[2][0] == 'ets':
                #     e[2] = 'etsportback'
                # else:
                e[1] = e[1] + e[2][0]
                e[2] = 'base'
            except:
                continue
            # e[2] = e[2][0] + 'superduty' + e[2][2]
            edmunds_index = ''.join([e[i] for i in [0, 1, 2, 3]])
            edmunds_index = re.sub(r'[ -]', '', edmunds_index)
            edmunds_index = re.sub(r'wagon', '', edmunds_index)
            edmunds_index = re.sub(r'sport', '', edmunds_index)
            edmunds_index = re.sub(r'cargo', '', edmunds_index)
            edmunds_index = re.sub(r'econoline', '', edmunds_index)
            edmunds_index = re.sub(r'suburban', '', edmunds_index)
            if edmunds_index not in edmunds_dict:
                edmunds_dict[edmunds_index] = e[4]
        for f in fire_lower:
            fire_index = ''.join([f[i] for i in [0, 1, 2, 3]])
            fire_index = re.sub(r'[ &-]', '', fire_index)
            # fire_index = re.sub(r'wagon', '', fire_index)
            fire_index = re.sub(r'sportback', '', fire_index)
            fire_index = re.sub(r'wagon', '', fire_index)
            fire_index = re.sub(r'econoline', '', fire_index)
            fire_index = re.sub(r'suburban', '', fire_index)
            # fire_index = re.sub(r'club', '', fire_index)
            if fire_index not in fire_dict:
                fire_dict[fire_index] = (f[4], f[5])

        for e_key in edmunds_dict:
            # if 'lancer' in e_key:
            #     print(e_key)
            for f_key in fire_dict:
                # if 'econoline' in f_key:
                #     print(f_key)
                if (e_key in f_key) or (f_key in e_key):
                    e_id = edmunds_dict[e_key]
                    f_id = fire_dict[f_key][0]
                    flag = fire_dict[f_key][1]
                    flag += 1
                    try:
                        print(e_key, e_id, f_id)
                        results.append(e_key)
                        # continue
                        cursor.execute('UPDATE car_features SET '
                                       'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
                                       'WHERE id=%s' % (f_id, e_id))
                        cursor.execute('UPDATE car_styles3 SET flag=%d WHERE id=%s' % (flag, f_id))
                        logger.debug('%s has update' % ((e_key, e_id, f_id),))
                    except Exception as e:
                        connect.rollback()
                        logger.debug('%s' % (e))
                    finally:
                        connect.commit()
        print(len(results))
        # break
    #
    # for e in edmunds_car:
    #     e[2] = e[2].split(' ')
    #     if len(e[2]) < 3:
    #         e[2] = 'base'
    #     else:
    #         e[2] = ''.join(e[2])
    #     edmunds_index = ''.join(e[:3])
    #     edmunds_index = re.sub(r'[ -]', '', edmunds_index)
    #     for f in fire_car:
    #         fire_index = ''.join(f[:3])
    #         fire_index = re.sub(r'[ -]', '', fire_index)
    #         # if edmunds_index in fire_index and e[3]==f[3] and len(edmunds_index)< len(fire_index):
    #         if ((fire_index in edmunds_index) or (edmunds_index in fire_index)) and f[3]==e[3]:
    #             intersection.append([e, f])
    #             logger.debug('%s' % ((e, f),))
    #             try:
    #                 cursor.execute('UPDATE car_features SET '
    #                                'tire_pressure=(SELECT tire_pressure FROM car_styles3 WHERE id=%s) '
    #                                'WHERE id=%s' % (f[4], e[4]))
    #             except Exception as e:
    #                 connect.rollback()
    #                 logger.debug('%s' %(e))
    #             finally:
    #                 connect.commit()
    #             break

    cursor.close()
    connect.close()
