from pymongo import MongoClient
import configparser
from tools import change_to_time_year_month_day_string
from datetime import datetime

cf = configparser.ConfigParser()
cf.read('configure.conf')


def get_db():
    host = cf.get('db', 'HOST')
    port = int(cf.get('db', 'PORT'))
    conn = MongoClient(host, port)
    # connect db
    db = conn.QunWeibo
    return db, conn


def get_collection(flag, db):
    # db = get_db()[0]
    # conn = get_db()[1]
    my_collection = db.temp_test
    if 'qun_weibo_id' in flag:
        my_collection = db.qun_weibo_id
    if 'qun_comments' in flag:
        my_collection = db.qun_comments
    if 'skip_qun_comments' in flag:
        my_collection = db.skip_qun_comments

    return my_collection


def insert_result(flag, data_list, db):
    my_collection = get_collection(flag, db)

    print(len(data_list))
    my_collection.insert(data_list)
    print('insert data to mongodb.....')


def find_all(flag, db):
    temp_list = []
    my_collection = get_collection(flag, db)
    cursor = my_collection.find({}, {'_id': 0})
    # base_time = get_date(days)
    for item in cursor:
        # create_time_datetime = change_to_year_month_day_datetime(item['create_time'])
        # if create_time_datetime > base_time:
        temp_list.append(item)
    return temp_list


def find_ids_by_more_than_the_base_day(flag, db, year, month, day):
    temp_list = []
    my_collection = get_collection(flag, db)
    print(year, month, day)
    # cursor = my_collection.find({"create_time": {'$gt': datetime(year, month , day)}}, {'_id': 0})
    cursor = my_collection.find({"weibo_create_time": {'$gt': datetime(year, month, day)}}, {'_id': 0}).sort(
        'weibo_create_time', -1)
    # base_time = get_date(days)
    for item in cursor:
        temp_list.append(item)
        # create_time_datetime = change_to_year_month_day_datetime(item['create_time'])
        # if create_time_datetime > base_time:
        #     temp_list.append(item['id'])
    return temp_list


def find_comments_by_day(flag, db, year, month, day, second_year, second_month, second_day):
    temp_list = []
    my_collection = get_collection(flag, db)
    print(year, month, day)
    # cursor = my_collection.find({"create_time": {'$gt': datetime(year, month , day)}}, {'_id': 0})
    print(second_year, second_month, second_day)
    cursor = my_collection.find({"weibo_create_time": {'$gt': datetime(year, month, day),
                                                       '$lt': datetime(second_year, second_month, second_day+1)}},
                                {'_id': 0}).sort(
        'weibo_create_time', -1)
    # base_time = get_date(days)
    for item in cursor:
        print(item)
        temp_list.append(item)
        # create_time_datetime = change_to_year_month_day_datetime(item['create_time'])
        # if create_time_datetime > base_time:
        #     temp_list.append(item['id'])
    return temp_list


# get the records sorted by create_time
def find_ids_by_sorted_create_time(flag, db, num):
    temp_list = []
    my_collection = get_collection(flag, db)
    cursor = my_collection.find({}, {'_id': 0}).sort('create_time', -1).limit(num)
    for item in cursor:
        temp_list.append(item)
    return temp_list


def find_result(flag, db):
    temp_list = []
    my_collection = get_collection(flag, db)

    cursor = my_collection.find({'result': 'no'}, {'_id': 0})
    for item in cursor:
        temp_list.append(item)
    return temp_list


def update_result(flag, db, data):
    my_collection = get_collection(flag, db)
    # cursor_find = []
    cursor_update = {}
    if 'qun_weibo_id' in flag:
        print('-------------------updat result json ----------------------------')
        # data['create_time'] = change_to_year_month_day_datetime(data['create_time'])
        result_json = {'weibo_id': data['weibo_id'], 'text': data['text'], 'weibo_create_time': data['weibo_create_time']}
        print(result_json)
        cursor_update = my_collection.update(
            {'weibo_id': data['weibo_id']},
            {'$set': {'text': data['text'], 'weibo_create_time': data['weibo_create_time']}}, True, True)

    if 'qun_comments' in flag or 'skip_qun_comments' in flag:
        print('-------------------update result json ----------------------------')
        # record = {'weibo_id': str(weibo_id), 'create_time': create_time, 'id': user_id, 'name': name,
        #                   'floor_number': comment_floor_number}
        # create_time_string = change_to_time_year_month_day_string(data['create_time'])
        result_json = {'weibo_id': data['weibo_id'], 'create_time': data['create_time'],
                       'user_id': data['id'],
                       'name': data['name'],
                       'floor_number': data['floor_number'], 'weibo_create_time': data['weibo_create_time']}
        print(result_json)
        cursor_update = my_collection.update(
            {'weibo_id': data['weibo_id'], 'user_id': data['id']},
            {'$set': {'name': data['name'], 'floor_number': data['floor_number'],
                      'create_time': data['create_time'], 'weibo_create_time': data['weibo_create_time']}}, True, True)

    print('-------------------------- update info ---------------------------')
    print(cursor_update)
    if cursor_update['nModified'] == 1:
        print('update...success..')


def close_db(conn):
    conn.close()

# new_db = get_db()
# temp_list = find_comments_by_day('qun_comments', new_db[0], 2018, 11, 18, 2018,11,21)
# # # temp_list = find_ids_by_more_than_the_base_day('qun_weibo_id', new_db[0], 2018, 11, 17)
# print(temp_list)
# close_db(new_db[1])
