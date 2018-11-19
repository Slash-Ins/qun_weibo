from pymongo import MongoClient
import configparser
from tools import change_to_year_month_day_datetime,get_date

cf = configparser.ConfigParser()
cf.read('configure.conf')


def get_db():
    host = cf.get('db', 'HOST')
    port = int(cf.get('db', 'PORT'))
    conn = MongoClient(host, port)
    # 连接mydb数据库，没有则自动创建
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

def find_ids(flag, db, days):
    temp_list = []
    my_collection = get_collection(flag, db)
    cursor = my_collection.find({}, {'_id': 0})
    base_time = get_date(days)
    for item in cursor:
        create_time_datetime = change_to_year_month_day_datetime(item['create_time'])
        if create_time_datetime > base_time:
            temp_list.append(item['id'])
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
    if 'qun_weibo_id':
        print('-------------------updat result json ----------------------------')
        result_json = {'id': data['id'], 'text': data['text'], 'create_time': data['create_time']}
        print(result_json)
        cursor_update = my_collection.update(
            {'id': data['id']},
            {'$set': {'text': data['text'], 'create_time': data['create_time']}}, True, True)

    # if 'st' in flag:
    #     print('-------------------updat result json ----------------------------')
    #     result_json = {'state': data['state'], 'zip_code': data['zip_code'],
    #                    'quote_url': data['quote_url'], 'result': data['result']}
    #     print(result_json)
    #     cursor_update = my_collection.update({'state': data['state'], 'zip_code': data['zip_code']},
    #                                          {'$set': {'quote_url': data['quote_url'], 'result': data['result']}}, True,
    #                                          True)

    print('-------------------------- update info ---------------------------')
    print(cursor_update)
    if cursor_update['nModified'] == 1:
        print('update...success..')


def close_db(conn):
    conn.close()
