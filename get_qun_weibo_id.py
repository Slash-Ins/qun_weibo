import datetime
import time

import requests
import json
from db import get_db, close_db, update_result, find_ids_by_more_than_the_base_day
from tools import cmt_change_to_datetime, change_to_time_year_month_day_string, change_to_time_string, \
    change_to_datetime,clean

from_source = '108A093010'
phone_name = 'iphone'
network_type = 'wifi'
s = 'aaaaaaaa'


def get_weibo_ids(gsid, get_id_count):
    # gsid = '_2A252zVACDeRxGeBL61YU8i3Jzj2IHXVT2-TKrDV6PUJbkdAKLRPukWpNR0__VwTYwMaWTGKaxujNmOv8-3CN0Zlf'
    # from_source = '108A093010'
    # phone_name = 'iphone'
    # network_type = 'wifi'
    # s = 'aaaaaaaa'
    # count = '20'
    # is_show_bulletin = '2'
    # id = '4297334122116398'
    # id = '4296971344358254'
    base_url = 'https://mapi.weibo.com/2/statuses/page_timeline'
    flow = '1'
    uid = '6504523551'
    # get_id_count = 20
    oid = '1022:2304914261430515326918'

    get_weibo_ids_url = base_url + '?gsid=' + gsid + '&from=' + from_source + '&c=' + phone_name + '&networktype=' \
                        + network_type + '&s=' + s + '&flow=' + flow

    params = {'uid': uid, 'count': get_id_count, 'oid': oid}
    print(get_weibo_ids_url)
    res = requests.post(get_weibo_ids_url, params)
    req.encoding = 'gbk'

    # res_text = res.text
    # res_json = json.load(res_text)
    res_json = req.json()
    print(res_json)
    print(len(res_json['statuses']))

    weibo_ids_list = []
    # temp_json = {}
    json_list = []
    for weibo in res_json['statuses']:
        # print(weibo['id'])
        # print(weibo['created_at'])
        # print(weibo['text'])
        weibo_create_time = cmt_change_to_datetime(weibo['created_at'])
        # print(weibo_create_time)
        # weibo_create_time_string = change_to_time_string(weibo_create_time)
        # print(weibo_create_time_string)
        temp_json = {'weibo_id': str(weibo['id']), 'text': weibo['text'],
                     'weibo_create_time': weibo_create_time}
        print(temp_json)
        json_list.append(temp_json)
        weibo_ids_list.append(str(weibo['id']))
    return json_list


def get_qun_weibo_comments(gsid, id):
    # gsid = '_2A252zVACDeRxGeBL61YU8i3Jzj2IHXVT2-TKrDV6PUJbkdAKLRPukWpNR0__VwTYwMaWTGKaxujNmOv8-3CN0Zlf'
    # from_source = '108A093010'
    # phone_name = 'iphone'
    # network_type = 'wifi'
    # s = 'aaaaaaaa'
    get_comments_count = '20'
    is_show_bulletin = '2'
    flow = '1'
    # weibo_id = '4292245878510166'
    comment_url = 'https://mapi.weibo.com/2/comments/build_comments'
    get_comment_url = comment_url + '?gsid=' + gsid + '&from=' + from_source + '&c=' + phone_name + '&networktype=' \
                      + network_type + '&s=' + s + '&count=' + get_comments_count + '&is_show_bulletin=' + is_show_bulletin + '&id=' + id + '&flow=' + flow
    print('start: ' + get_comment_url)
    req = requests.get(get_comment_url)
    req.encoding = 'utf-8'
    res = req.json()
    count = 0

    comment_list = []

    # first comment
    # # qun weibo create time
    # create_time = res['status']['created_at']

    # qun weibo comments total number
    total_number = res['total_number']

    print(res['root_comments'])
    print(len(res['root_comments']))
    count = count + len(res['root_comments'])
    first_comments = res['root_comments']

    # 数据没请求到，重新请求
    if len(first_comments) == 0:
        print('-------------- repeat req -------------')
        time.sleep(5)
        print(get_comment_url)
        req = requests.get(get_comment_url)
        req.encoding = 'utf-8'
        res = req.json()
        print(res['root_comments'])
        print(len(res['root_comments']))
        count = count + len(res['root_comments'])
        first_comments = res['root_comments']

    for comments in first_comments:
        comment_list.append(comments)

    while True:
        max_id = str(res['max_id'])
        print('max_id: ' + str(res['max_id']))
        if int(max_id) != 0:
            print('---------- get 20 items comments --------')
            temp_get_comment_url = get_comment_url + '&max_id=' + max_id
            print(temp_get_comment_url)
            req = requests.get(temp_get_comment_url)
            req.encoding = 'utf-8'
            res = req.json()
            print(res['root_comments'])
            print(len(res['root_comments']))
            count = count + len(res['root_comments'])
            temp_comments = res['root_comments']

            # 数据没请求到，重新请求
            if len(temp_comments) == 0:
                print('-------------- repeat req -------------')
                time.sleep(5)
                print(temp_get_comment_url)
                req = requests.get(temp_get_comment_url)
                req.encoding = 'utf-8'
                res = req.json()
                print(res['root_comments'])
                print(len(res['root_comments']))
                count = count + len(res['root_comments'])
                temp_comments = res['root_comments']

            for comments in temp_comments:
                comment_list.append(comments)
            # print(res['max_id'])
        else:
            print('-------------- get comments end --------------------')
            break
    print(count)
    print(total_number)
    print(comment_list)
    print(len(comment_list))
    return comment_list


def update_weibo_ids_to_db(data_list, new_db):
    for data in data_list:
        update_result('qun_weibo_id', new_db, data)

#
# gsid = '_2A2526vTUDeRxGeBL61YU8i3Jzj2IHXVTvg8crDV6PUJbkdAKLRfAkWpNR0__V1fpj7VmhYONjSzF3Tb63fcChvBJ'
# # current_day = datetime.datetime.now().day
# # # data_list = get_weibo_ids(gsid, current_day)
# data_list = get_weibo_ids(gsid, 31)
# print(len(data_list))
# print(data_list)

# get_qun_weibo_comments(gsid, '4292245878510166')
# new_db = get_db()
# update_weibo_ids_to_db(data_list, new_db[0])
#
# print(find_ids_by_more_than_the_base_day('qun_weibo_id', new_db[0], 2018, 10,24))
# close_db(new_db[1])
