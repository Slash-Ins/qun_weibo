from pymongo import MongoClient
import configparser

cf = configparser.ConfigParser()
cf.read('configure.conf')


def get_db():
    host = cf.get('db', 'HOST')
    port = int(cf.get('db', 'PORT'))
    conn = MongoClient(host, port)
    # 连接mydb数据库，没有则自动创建
    db = conn.CensusToQuote
    return db, conn


def get_collection(flag, db):
    # db = get_db()[0]
    # conn = get_db()[1]

    if 'ifp' in flag:
        my_collection = db.ifp_census_to_quote
    elif 'obama' in flag:
        my_collection = db.obama_census_to_quote
    elif 'st' in flag:
        my_collection = db.st_census_to_quote
    else:
        my_collection = db.ifp_census_to_quote
    return my_collection


def insert_result(flag, db):
    # file_list = get_prod_line_report_file_name(flag)
    # my_collection = get_collection(flag, db)
    #
    # for file in file_list:
    #     data_list = data_result(file)
    #     print(len(data_list))
    #     my_collection.insert(data_list)
    #     print('insert data to mongodb.....')
    return


def find_all(flag, db):
    # temp_list = []
    # my_collection = get_collection(flag, db)
    # cursor = my_collection.find({}, {'_id': 0})
    # for item in cursor:
    #     temp_list.append(item)
    # return temp_list
    return


def find_no_result(flag, db):
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
    if 'ifp' in flag or 'obama' in flag:
        print('-------------------updat result json ----------------------------')
        result_json = {'state': data['state'], 'zip_code': data['zip_code'], 'income': data['income'],
                       'quote_url': data['quote_url'], 'result': data['result']}
        print(result_json)
        cursor_update = my_collection.update(
            {'state': data['state'], 'zip_code': data['zip_code'], 'income': data['income']},
            {'$set': {'quote_url': data['quote_url'], 'result': data['result']}}, True, True)

    if 'st' in flag:
        print('-------------------updat result json ----------------------------')
        result_json = {'state': data['state'], 'zip_code': data['zip_code'],
                       'quote_url': data['quote_url'], 'result': data['result']}
        print(result_json)
        cursor_update = my_collection.update({'state': data['state'], 'zip_code': data['zip_code']},
                                             {'$set': {'quote_url': data['quote_url'], 'result': data['result']}}, True,
                                             True)

    print('-------------------------- update info ---------------------------')
    print(cursor_update)
    if cursor_update['nModified'] == 1:
        print('update...success..')


def close_db(conn):
    conn.close()
