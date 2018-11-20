import requests
import operator
from tools import change_to_datetime, change_to_time_string, cmt_change_to_datetime, list_duplicates, del_dup, \
    check_dup, search_excel_row_col, get_excel_max_rows_cols
import xlrd
from xlutils.copy import copy
from get_qun_weibo_id import get_weibo_ids, get_qun_weibo_comments
import time
# from count import count_daka
from db import get_db, close_db, find_ids_by_more_than_the_base_day, update_result, find_all

# https://mapi.weibo.com/2/comments/build_comments?gsid=_2A252zVACDeRxGeBL61YU8i3Jzj2IHXVT2-TKrDV6PUJbkdAKLRPukWpNR0__VwTYwMaWTGKaxujNmOv8-3CN0Zlf&from=108A093010&c=iphone&networktype=wifi&s=aaaaaaaa&lang=zh_CN&ft=0&aid=01ArzgVId_Zvp4PxhcrQFbRrAQ7rwXnRtWAD8TTrm2H9yg9EI.&is_reload=1&is_append_blogs=1&mid=4296603013573659&refresh_type=1&uicode=10000002&count=163&trim_level=1&moduleID=feed&is_show_bulletin=2&fetch_level=0&_status_id=4296603013573659&id=4296603013573659&since_id=0&is_mix=1&page=0
gsid = '_2A2526vTUDeRxGeBL61YU8i3Jzj2IHXVTvg8crDV6PUJbkdAKLRfAkWpNR0__V1fpj7VmhYONjSzF3Tb63fcChvBJ'
from_source = '108A093010'
phone_name = 'iphone'
network_type = 'wifi'
s = 'aaaaaaaa'
get_comments_count = '20'
is_show_bulletin = '2'

weibo_ids_list = []
new_db = get_db()
temp_list = find_ids_by_more_than_the_base_day('qun_weibo_id', new_db[0], 2018, 10, 23)
print(temp_list)
for temp in temp_list:
    weibo_ids_list.append(temp['id'])

record = {}
comment_list = []

for weibo_id in weibo_ids_list:
    print('************ weibo ids **********')
    print(weibo_id)
    comment_url = 'https://mapi.weibo.com/2/comments/build_comments'
    print(gsid)
    print(from_source)
    get_comment_url = comment_url + '?gsid=' + gsid + '&from=' + from_source + '&c=' + phone_name + '&networktype=' \
                      + network_type + '&s=' + s + '&count=' + get_comments_count + '&is_show_bulletin=' + is_show_bulletin + '&id=' + weibo_id
    print(get_comment_url)
    req = requests.get(get_comment_url)
    res = req.json()
    print(res['total_number'])

    # 微博发布时间
    create_time = res['status']['created_at']
    print(create_time)
    weibo_create_time = cmt_change_to_datetime(create_time)
    print(weibo_create_time)
    weibo_create_time_string = change_to_time_string(weibo_create_time)
    print(weibo_create_time_string)

    # # 微博返回评论数量
    # print(len(res['root_comments']))
    # # 实际评论数量
    # count = 0
    # 构造单个评论爬取结果

    qun_comments_list = get_qun_weibo_comments(gsid, weibo_id)

    # 获取评论信息
    for comment in qun_comments_list:
        # print(comment)
        name = comment['user']['name']
        comment_create_time = comment['created_at']
        user_id = comment['user']['id']
        comment_floor_number = comment['floor_number']

        create_time = cmt_change_to_datetime(comment_create_time)
        # create_time = int(time.mktime(create_time.timetuple()))
        create_time = change_to_time_string(create_time)

        record = {'weibo_id': str(weibo_id), 'create_time': create_time, 'id': user_id, 'name': name,
                  'floor_number': comment_floor_number}
        comment_list.append(record)

print(comment_list)
# new_db = get_db()
for comment in comment_list:
    update_result('qun_comments', new_db[0], comment)
print(find_all('qun_comments', new_db[0]))
# print(find_ids_by_more_than_the_base_day('qun_weibo_id', new_db[0], 2018, 10,23))
close_db(new_db[1])
