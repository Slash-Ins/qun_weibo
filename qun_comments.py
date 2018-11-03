import requests
import operator
from tools import change_to_datetime, change_to_time_string, cmt_change_to_datetime, list_duplicates, del_dup, \
    check_dup, search_excel_row_col, get_excel_max_rows_cols
import xlrd
from xlutils.copy import copy
from get_qun_weibo_id import get_weibo_ids, get_qun_weibo_comments
import time
from count import count_daka

# https://mapi.weibo.com/2/comments/build_comments?gsid=_2A252zVACDeRxGeBL61YU8i3Jzj2IHXVT2-TKrDV6PUJbkdAKLRPukWpNR0__VwTYwMaWTGKaxujNmOv8-3CN0Zlf&from=108A093010&c=iphone&networktype=wifi&s=aaaaaaaa&lang=zh_CN&ft=0&aid=01ArzgVId_Zvp4PxhcrQFbRrAQ7rwXnRtWAD8TTrm2H9yg9EI.&is_reload=1&is_append_blogs=1&mid=4296603013573659&refresh_type=1&uicode=10000002&count=163&trim_level=1&moduleID=feed&is_show_bulletin=2&fetch_level=0&_status_id=4296603013573659&id=4296603013573659&since_id=0&is_mix=1&page=0
gsid = '_2A252zVACDeRxGeBL61YU8i3Jzj2IHXVT2-TKrDV6PUJbkdAKLRPukWpNR0__VwTYwMaWTGKaxujNmOv8-3CN0Zlf'
from_source = '108A093010'
phone_name = 'iphone'
network_type = 'wifi'
s = 'aaaaaaaa'
get_comments_count = '20'
is_show_bulletin = '2'
# id = '4297334122116398'
# id = '4296971344358254'
# weibo_id = '4291521454660997'
file = 'qun_comments_data_new.xlsx'
# more_than_200 = []

# weibo_ids_list = get_weibo_ids(gsid, 28)
weibo_ids_list = get_weibo_ids(gsid, 30)

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
    record = {}
    comment_list = []

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

        record = {'create_time': create_time, 'id': user_id, 'name': name, 'floor_number': comment_floor_number}
        comment_list.append(record)

    sorted_x = comment_list
    print(sorted_x)

    # 去重删除
    dup_list = []
    for dup in sorted(list_duplicates(check_dup(sorted_x))):
        dup_list.append(dup)

    # print(sorted_x[53])
    # print(sorted_x[166])
    # loop_dup_list = []

    for i in range(len(dup_list)):
        save_index = 0

        if len(dup_list[i][1]) > 2:
            save_index = dup_list[i][1][0]
            print('--------- save_index ----------')
            print(sorted_x[save_index])

        loop_dup_list = []
        del_dup_list = []
        for dup in sorted(list_duplicates(check_dup(sorted_x))):
            loop_dup_list.append(dup)
        print('-----  dup list ----')
        print(loop_dup_list)
        del_dup_list.append(loop_dup_list[0])
        del_dup(del_dup_list, sorted_x, save_index)

    # 校验是否删除成功
    dup_list = []
    for dup in sorted(list_duplicates(check_dup(sorted_x))):
        print(dup)
        dup_list.append(dup)
    print('----- dup list ----')
    print(dup_list)
    if len(dup_list) == 0:
        print('all comments are not dup......')

    print(sorted_x)

    # 校验最后一条评论是否有超过24小时
    last_comment_create_time = change_to_datetime(sorted_x[0]['create_time'])
    print(last_comment_create_time)
    if (last_comment_create_time - weibo_create_time).days < 1:
        print('all comments create time < 24 hours...')
    else:
        print('no')
        delete_list = []
        for i in range(len(sorted_x)):
            comment_create_time = change_to_datetime(sorted_x[i]['create_time'])
            if (comment_create_time - weibo_create_time).days > 1:
                print('comment create time > 24 hours, deleting... ')
                print(sorted_x[i])
                delete_list.append(sorted_x[i])
                # del sorted_x[i]
        if len(delete_list) > 0:
            for delete in delete_list:
                sorted_x.remove(delete)
                print('delete.....')
                print(delete)

    print('----------- weibo create time ---------')
    print(weibo_create_time_string)
    print(weibo_create_time_string[0:10])
    for sort in sorted_x:
        sort['create_time'] = weibo_create_time_string[0:10]
    # init_excel(file, 0)

    # file = 'qun_weiobo_comments.xlsx'
    rb = xlrd.open_workbook(file)
    wb = copy(rb)
    ws = wb.get_sheet(0)

    excel_max_rows_cols = get_excel_max_rows_cols(file, 0)
    max_row = excel_max_rows_cols[0]
    # print(excel_max_rows_cols)
    # max_row = max_row + 1
    for i in range(len(sorted_x)):
        if 'false' in search_excel_row_col(file, sorted_x[i]['id'])[0]:
            print('$$$$$$$$$$$$$$$$$$$$$$$$')
            # excel_max_rows_cols = get_excel_max_rows_cols(file, 0)
            print(max_row)
            # print(excel_max_rows_cols[1])
            # ws.deleteRow()

            print('$$$$$$$$$$$$$$$$$$$$$$$$')

            ws.write(max_row, 0, str(sorted_x[i]['id']))
            ws.write(max_row, 1, sorted_x[i]['name'])
            max_row = max_row + 1
    print('max_row: ' + str(max_row))
    wb.save(file)

    temp_count =0
    print('--------------- last sorted list ----------')
    print(sorted_x)
    print(len(sorted_x))
    for comment in sorted_x:
        # print(comment['create_time'][0:10])
        temp_id = search_excel_row_col(file, str(comment['id']))
        temp_date = search_excel_row_col(file, comment['create_time'])
        print('&&&&&&&&&&&&&&&&&&&&&&')
        print(comment['create_time'])
        print(comment['id'])
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

count_daka(file, 0)

#
# print('--------------- skip weibo ---------------')
# print(more_than_200)
