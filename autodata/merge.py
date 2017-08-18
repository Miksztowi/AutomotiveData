import MySQLdb
import logging
import re
from functools import wraps
import sys
import time
import autodata.settings as settings

connect = MySQLdb.connect(
    host=settings.DB_HOST, port=settings.DB_PORT,
    user=settings.DB_USER, password=settings.DB_PASSWORD, database=settings.DB
)
cursor = connect.cursor()
logging.basicConfig(filename='merge.log', level="DEBUG")


def get_cars_lower():
    cursor.execute('SELECT make, model, submodel, year, id, flag FROM firestone_cars')
    fire_car = cursor.fetchall()
    cursor.execute('SELECT make, model, name, year, id FROM edmunds_cars WHERE tire_pressure IS NULL')
    edmunds_car = cursor.fetchall()
    fire_lower = [[x.lower() if isinstance(x, str) else x for x in a] for a in fire_car]
    edmunds_lower = [[x.lower() if isinstance(x, str) else x for x in a] for a in edmunds_car]
    return edmunds_lower, fire_lower


def handle_submodel(name, start, end):
    submodel = name.split(' ')
    if 'dr' in submodel[0] or len(submodel) < 3:
        submodel = 'base'
    else:
        try:
            submodel = ''.join(submodel[start:end])
        except IndexError:
            return None
    return submodel


def update_mysql(e_key, e_id, f_id, flag):
    logger = logging.getLogger(sys._getframe(2).f_code.co_name)
    e_id = ','.join([str(x) for x in e_id])
    try:
        cursor.execute('UPDATE edmunds_cars SET '
                       'tire_pressure=(SELECT tire_pressure FROM firestone_cars WHERE id=%s) '
                       'WHERE id in (%s)' % (f_id, e_id))
        cursor.execute('UPDATE firestone_cars SET flag=%d WHERE id=%s' % (flag, f_id))
        logger.debug('%s has update' % ((e_key, e_id, f_id),))
    except MySQLdb.Error as e :
        connect.rollback()
        logger.warning('%s' %(e))
    finally:
        connect.commit()


def clean_data(data):

    data = re.sub(r'mx-5', '', data)
    data = re.sub(r'b-series-(truck)?', '', data)
    data = re.sub(r'minivan', '', data)
    data = re.sub(r'pickup', '', data)
    data = re.sub(r'econoline', '', data)
    data = re.sub(r'truck', '', data)
    data = re.sub(r'malibu-maxx', '', data)
    data = re.sub(r'van', '', data)
    data = re.sub(r'hybrid', '', data)
    data = re.sub(r'savana', '', data)
    data = re.sub(r'cargo', '', data)
    data = re.sub(r'new', '', data)
    data = re.sub(r'passenger', '', data)
    data = re.sub(r'model', '', data)
    data = re.sub(r'convertible', '', data)
    data = re.sub(r'sportwagen', '', data)
    data = re.sub(r'coupe', '', data)
    data = re.sub(r'quattro', '', data)
    data = re.sub(r'suburban', '', data)
    data = re.sub(r'solara', '', data)
    # data = re.sub(r'lumina', '', data)
    data = re.sub(r'mazdaspeed', '', data)
    data = re.sub(r'lt\d', 'lt', data)
    data = re.sub(r'xl', '', data)
    data = re.sub(r'club', '', data)
    data = re.sub(r'civic', '', data)
    data = re.sub(r'sportback', '', data)
    data = re.sub(r'econoline-wagon', '', data)
    data = re.sub(r'e-series-van', '', data)
    data = re.sub(r'wagon', '', data)
    data = re.sub(r'g(?P<name>\d{4})', r'\g<name>', data)
    data = re.sub(r'(?P<name>b\d{4})i', r'\g<name>', data)
    data = re.sub(r'b-series-pickup', r'', data)
    data = re.sub(r'cl-class', '', data)
    data = re.sub(r'cls-class', '', data)
    data = re.sub(r'clk-class', '', data)
    data = re.sub(r'e-class', '', data)
    data = re.sub(r'and', '', data)
    data = re.sub(r'c-class', '', data)
    data = re.sub(r'g-class', '', data)
    data = re.sub(r'gla-class', '', data)
    data = re.sub(r'gl-class', '', data)
    data = re.sub(r'gl-class', '', data)
    data = re.sub(r'g-sedan', '', data)
    data = re.sub(r'sedan', '', data)
    data = re.sub(r'm-class', '', data)
    data = re.sub(r'golf', '', data)
    data = re.sub(r'sl-class', '', data)
    data = re.sub(r's-class', '', data)
    data = re.sub(r'e-series-wagon', '', data)
    data = re.sub(r'slk-class', '', data)
    data = re.sub(r'e-class', '', data)
    data = re.sub(r'[ &-]', '', data)
    return data


def find_intersection(edmunds_dict, fire_dict, each_in=False):
    result_length = 0
    if each_in:
        for e_key in edmunds_dict:
            for f_key in fire_dict:
                if (e_key in f_key) or (f_key in e_key):
                    e_id = edmunds_dict[e_key]
                    f_id = fire_dict[f_key][0]
                    flag = fire_dict[f_key][1]
                    flag += 1
                    result_length += len(e_id)
                    update_mysql(e_key, e_id, f_id, flag)
    else:
        for e_key in edmunds_dict:
            if e_key in fire_dict:
                e_id = edmunds_dict[e_key]
                f_id = fire_dict[e_key][0]
                flag = fire_dict[e_key][1]
                flag += 1
                result_length += len(e_id)
                update_mysql(e_key, e_id, f_id, flag)


    print(sys._getframe(1).f_code.co_name, result_length)
    return result_length


def handle_position(e_position, f_position, sub_position, is_clean=False):
    edmunds_lower, fire_lower = get_cars_lower()
    make, model, sub, year, id, flag = range(6)
    edmunds_dict = {}
    fire_dict = {}
    submodel_pos = sub_position['submodel']
    if sub_position.get('model'):
        model_pos = sub_position['model']
        for e in edmunds_lower:
            e[model] += handle_submodel(name=e[sub], start=model_pos['start'], end=model_pos['end'])
            e[sub] = handle_submodel(name=e[sub], start=submodel_pos['start'], end=submodel_pos['end'])

            edmunds_index = ''.join([e[i] for i in e_position])
            edmunds_index = clean_data(edmunds_index) if is_clean else edmunds_index
            if edmunds_index not in edmunds_dict:
                edmunds_dict[edmunds_index] = [e[id]]
            else:
                edmunds_dict[edmunds_index].append(e[id])

    else:
        for e in edmunds_lower:
            e[sub] = handle_submodel(name=e[sub], start=submodel_pos['start'], end=submodel_pos['end'])
            edmunds_index = ''.join([e[i] for i in e_position])
            edmunds_index = clean_data(edmunds_index) if is_clean else edmunds_index
            if edmunds_index not in edmunds_dict:
                edmunds_dict[edmunds_index] = [e[id]]
            else:
                edmunds_dict[edmunds_index].append(e[id])

    for f in fire_lower:
        fire_index = ''.join([f[i] for i in f_position])
        fire_index = clean_data(fire_index) if is_clean else fire_index
        if fire_index not in fire_dict:
            fire_dict[fire_index] = (f[id], f[flag])
    return edmunds_dict, fire_dict


def direct_merge():
    e_position = [0, 1, 2, 3]
    f_position = [0, 1, 2, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position)
    find_intersection(edmunds_dict, fire_dict)


def step_merge():
    for step in range(1,6):
        for index in range(8):
            e_position = [0, 1, 2, 3]
            f_position = [0, 1, 2, 3]
            sub_position = {
                'submodel': {
                    'start': index,
                    'end': index + step,
                }
            }
            edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
            find_intersection(edmunds_dict, fire_dict)


def submodel_model_merge():
    e_position = [0, 2, 3]
    f_position = [0, 1, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict)


    sub_position = {
        'submodel': {
            'start': 0,
            'end': 2,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict)

    sub_position = {
        'submodel': {
            'start': 0,
            'end': 3,
        }
    }

    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict)

    e_position = [0, 1, 2, 3]
    f_position = [0, 1, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict)


def model_submodel_merge():
    e_position = [0, 1, 3]
    f_position = [0, 2, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict)

    e_position = [0, 1, 3]
    f_position = [0, 1, 2, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict)


def position_merge():
    e_position = [0, 1, 2, 3]
    f_position = [0, 1, 2, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        },
        'model':{
            'start': 1,
            'end': 2,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict)

    e_position = [0, 1, 3]
    f_position = [0, 1, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        },
        'model': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict)


def all_no_use_submodel():

    e_position = [0, 1, 3]
    f_position = [0, 1, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict)


def each_in():
    e_position = [0, 1, 2, 3]
    f_position = [0, 1, 2, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict, each_in=True)


def other_merge():
    e_position = [0, 1, 2, 3]
    f_position = [0, 1, 3]
    sub_position = {
        'submodel': {
            'start': 3,
            'end': 4,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    for e in edmunds_dict:
        if 'mazda' in e:
            print(e)
    find_intersection(edmunds_dict, fire_dict, each_in=True)

    e_position = [0, 2, 3]
    f_position = [0, 1, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict, each_in=True)

    e_position = [0, 1, 3]
    f_position = [0, 1, 3]
    sub_position = {
        'submodel': {
            'start': 1,
            'end': 2,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict, each_in=True)

    e_position = [0,  1, 2, 3]
    f_position = [0,  1, 2, 3]
    sub_position = {
        'submodel': {
            'start': 0,
            'end': 1,
        }
    }
    edmunds_dict, fire_dict = handle_position(e_position, f_position, sub_position, is_clean=True)
    find_intersection(edmunds_dict, fire_dict, each_in=True)


def merge():
    start = time.perf_counter()
    direct_merge()
    step_merge()
    submodel_model_merge()
    model_submodel_merge()
    position_merge()
    all_no_use_submodel()
    each_in()
    other_merge()
    cost = time.perf_counter() - start
    print('all merge options have cost %s seconds' % (cost))


if __name__ == '__main__':
   merge()



