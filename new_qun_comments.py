import requests
from tools import change_to_datetime, change_to_time_string, cmt_change_to_datetime, list_duplicates, del_dup, \
    check_dup, search_excel_row_col, get_excel_max_rows_cols, get_date_before_today,change_to_time_year_month_day_string
import xlrd
from xlutils.copy import copy
from get_qun_weibo_id import get_weibo_ids, get_qun_weibo_comments,update_weibo_ids_to_db
from count import count_daka
from db import get_db, close_db, find_ids_by_more_than_the_base_day, update_result, find_all, get_collection, \
    find_ids_by_sorted_create_time,find_comments_by_day

# https://mapi.weibo.com/2/comments/build_comments?gsid=_2A252zVACDeRxGeBL61YU8i3Jzj2IHXVT2-TKrDV6PUJbkdAKLRPukWpNR0__VwTYwMaWTGKaxujNmOv8-3CN0Zlf&from=108A093010&c=iphone&networktype=wifi&s=aaaaaaaa&lang=zh_CN&ft=0&aid=01ArzgVId_Zvp4PxhcrQFbRrAQ7rwXnRtWAD8TTrm2H9yg9EI.&is_reload=1&is_append_blogs=1&mid=4296603013573659&refresh_type=1&uicode=10000002&count=163&trim_level=1&moduleID=feed&is_show_bulletin=2&fetch_level=0&_status_id=4296603013573659&id=4296603013573659&since_id=0&is_mix=1&page=0
gsid = '_2A2526vTUDeRxGeBL61YU8i3Jzj2IHXVTvg8crDV6PUJbkdAKLRfAkWpNR0__V1fpj7VmhYONjSzF3Tb63fcChvBJ'
from_source = '108A093010'
phone_name = 'iphone'
network_type = 'wifi'
s = 'aaaaaaaa'
get_comments_count = '20'
is_show_bulletin = '2'
new_db = get_db()


def get_after_the_date_weibo_comments(year, month, day):
    weibo_ids_list = []

    temp_list = find_ids_by_more_than_the_base_day('qun_weibo_id', new_db[0], year, month, day)
    # temp_list = find_ids_by_more_than_the_base_day('qun_weibo_id', new_db[0], 2018, 10, 23)
    print(temp_list)
    for temp in temp_list:
        weibo_ids_list.append(temp['id'])

    print('------------------------------ weibo_ids_list ----------------------')
    print(weibo_ids_list)
    comment_list = []
    skip_comment_list = []

    for weibo_id in weibo_ids_list:
        print('************ weibo ids **********')
        print(weibo_id)
        comment_url = 'https://mapi.weibo.com/2/comments/build_comments'
        print(gsid)
        print(from_source)
        get_comment_url = comment_url + '?gsid=' + gsid + '&from=' + from_source + '&c=' + phone_name + '&networktype=' \
                          + network_type + '&s=' + s + '&count=' + get_comments_count + '&is_show_bulletin=' + is_show_bulletin + '&id=' + weibo_id
        print(get_comment_url)
        try:
            req = requests.get(get_comment_url)
            res = req.json()
            print(res['total_number'])
        except:
            print('----------- error request ------')
            print(req.text)
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
            # create_time = change_to_time_string(create_time)

            record = {'weibo_id': str(weibo_id), 'create_time': create_time, 'id': user_id, 'name': name,
                      'floor_number': comment_floor_number, 'weibo_create_time':weibo_create_time}
            if (weibo_create_time-create_time).days > 1:
                print('-------------------- comments more than 24 hours, skip -------------------------')
                skip_comment_list.append(record)
            else:
                comment_list.append(record)
    print(comment_list)
    print(skip_comment_list)
    # new_db = get_db()

    for comment in comment_list:
        update_result('qun_comments', new_db[0], comment)
    print(find_all('qun_comments', new_db[0]))
    if len(skip_comment_list) > 0:
        for skip_comment in skip_comment_list:
            update_result('skip_qun_comments', new_db[0], skip_comment)
    print(find_all('skip_qun_comments', new_db[0]))


def get_comments_by_ids(data_list):
    weibo_ids_list = []
    comment_list = []
    skip_comment_list = []
    for temp in data_list:
        weibo_ids_list.append(temp['weibo_id'])

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
            # create_time = change_to_time_string(create_time)

            record = {'weibo_id': str(weibo_id), 'create_time': create_time, 'id': user_id, 'name': name,
                      'floor_number': comment_floor_number, 'weibo_create_time': weibo_create_time}
            if (weibo_create_time-create_time).days > 1:
                print('-------------------- comments more than 24 hours, skip -------------------------')
                skip_comment_list.append(record)
            else:
                comment_list.append(record)
    print(comment_list)
    print(skip_comment_list)
    # new_db = get_db()
    for comment in comment_list:
        update_result('qun_comments', new_db[0], comment)
    print(find_all('qun_comments', new_db[0]))
    if len(skip_comment_list) > 0:
        for skip_comment in skip_comment_list:
            update_result('skip_qun_comments', new_db[0], skip_comment)
    print(find_all('skip_qun_comments', new_db[0]))


def get_the_lastest_comments():
    # year = int(time.strftime('%Y'))
    # month = int(time.strftime('%m'))
    # day = int(time.strftime('%d'))
    # print(int(year), int(month), int(day))
    last_weibo_data_list = get_weibo_ids(gsid, 1)
    last_create_time_wb = last_weibo_data_list[0]['create_time']
    print(last_weibo_data_list[0]['create_time'])
    print(type(last_weibo_data_list[0]['create_time']))

    temp_list = find_ids_by_sorted_create_time('qun_comments', new_db[0], 1)
    # print(temp_list[0]['create_time'])
    # print(type(temp_list[0]['create_time']))
    last_create_time_db = temp_list[0]['create_time']
    # print(last_create_time_db)
    # print(type(last_create_time_db))
    if (last_create_time_wb - last_create_time_db).days >= 1:
        print('----- before last update : more than 1 day, begin to get the last 7 days weibo ids -------')
        the_last_week_weibo_ids_list = get_weibo_ids(gsid, 7)
        update_weibo_ids_to_db(the_last_week_weibo_ids_list, new_db[0])
        print('----- before last update : more than 1 day, begin to get the last 7 days comments -------')
        last_week_date_string = get_date_before_today(7)
        # print(last_week_date_string)
        last_week_date_list = last_week_date_string.split('-')
        # print(type(last_week_date_list))
        # print(last_week_date_list)
        print(int(last_week_date_list[0]), int(last_week_date_list[1]), int(last_week_date_list[2]))
        get_after_the_date_weibo_comments(int(last_week_date_list[0]), int(last_week_date_list[1]),
                                          int(last_week_date_list[2]))
    else:
        print('------- update the latest day comments -----------------')
        print(temp_list)
        get_comments_by_ids(temp_list)


def save_to_excel(data_list):
    file = 'qun_comments_data_new.xlsx'
    rb = xlrd.open_workbook(file)
    wb = copy(rb)
    sheet_index = 1
    ws = wb.get_sheet(sheet_index)

    excel_max_rows_cols = get_excel_max_rows_cols(file, sheet_index)
    max_row = excel_max_rows_cols[0]
    print('------------ max rows---------')
    print(excel_max_rows_cols)
    # max_row = max_row + 1
    for i in range(len(data_list)):
        if 'false' in search_excel_row_col(file,sheet_index, data_list[i]['user_id'])[0]:
            print('$$$$$$$$$$$$$$$$$$$$$$$$')
            # excel_max_rows_cols = get_excel_max_rows_cols(file, 0)
            print(max_row)
            # print(excel_max_rows_cols[1])
            # ws.deleteRow()

            print('$$$$$$$$$$$$$$$$$$$$$$$$')

            ws.write(max_row, 0, str(data_list[i]['user_id']))
            ws.write(max_row, 1, data_list[i]['name'])
            max_row = max_row + 1
    print('max_row: ' + str(max_row))
    wb.save(file)

    temp_count = 0
    print('--------------- last sorted list ----------')
    print(data_list)
    print(len(data_list))
    for comment in data_list:
        # print(comment['create_time'][0:10])
        temp_id = search_excel_row_col(file,sheet_index, str(comment['user_id']))
        temp_date_string = change_to_time_year_month_day_string(comment['create_time'])
        temp_date = search_excel_row_col(file, sheet_index, temp_date_string)
        print('&&&&&&&&&&&&&&&&&&&&&&')
        print(comment['create_time'])
        print(temp_date_string)
        print(comment['user_id'])
        print(temp_id[0])
        print(temp_date[1])
        temp_count = temp_count + 1
        print('&&&&&&&&&&&&&&&&&&&&&&')
        ws.write(int(temp_id[0]), int(temp_date[1]), '1')

        # if not len(search_excel_row_col(file, comment['id']) > 0:
        # ws.write(int(temp_id[0]), int(temp_date[1]), '')
    print('------------------ 每条微博插入数量 -----------')
    print(temp_count)
    wb.save(file)


    print('---------------- save excel success --------------------')
    count_daka(file, sheet_index)





# print(find_ids_by_more_than_the_base_day('qun_weibo_id', new_db[0], 2018, 11, 24))
# get_after_the_date_weibo_comments(2018, 10, 24)
# get_the_lastest_comments()

# 2018-11-18 _ 2018-11-20
temp_list = find_comments_by_day('qun_comments', new_db[0], 2018, 11, 18, 2018,11,21)
# # temp_list = find_ids_by_more_than_the_base_day('qun_weibo_id', new_db[0], 2018, 11, 17)
print(temp_list)

close_db(new_db[1])
save_to_excel(temp_list)
