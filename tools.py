import datetime
from datetime import timedelta

from collections import defaultdict
import xlrd
import xlwt
# import os
from xlutils.copy import copy
import calendar

def clean(data):
    if isinstance(data, str):
        return data.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    if isinstance(data, list):
        return [clean(item) for item in data]
    if isinstance(data, dict):
        return {clean(key): clean(value) for (key, value) in data.items()}
    return data



def cmt_change_to_datetime(time_string):
    format_string = '%a %b %d %H:%M:%S +0800 %Y'
    datetime_time = datetime.datetime.strptime(time_string, format_string)
    # print(datetime_time)
    return datetime_time
    # a = datetime.datetime.strptime(time_string, test)
    # b = datetime.datetime.strptime(time_string2, test)
    # print(type(a))
    # print(a)
    # print(b)
    # print((b-a).days)


def change_to_datetime(time_string):
    format_string = '%Y-%m-%d %H:%M:%S'
    datetime_time = datetime.datetime.strptime(time_string, format_string)
    # print(datetime_time)
    return datetime_time


def change_to_time_string(time):
    format_string = '%Y-%m-%d %H:%M:%S'
    time_string = time.strftime(format_string)
    return time_string


def change_to_time_year_month_day_string(time):
    format_string = '%Y-%m-%d'
    time_string = time.strftime(format_string)
    return time_string


def change_to_year_month_day_datetime(time_string):
    format_string = '%Y-%m-%d'
    datetime_time = datetime.datetime.strptime(time_string, format_string)
    # print(datetime_time)
    return datetime_time


def get_date_before_today(days):
    temp_time = datetime.datetime.now() - timedelta(days=days)
    temp_time_string = change_to_time_year_month_day_string(temp_time)
    # temp_time_year_month_day = change_to_year_month_day_datetime(temp_time_string)
    # return temp_time_year_month_day
    return temp_time_string


# 获取一段时间内的日期
# eg:start_date_string = 2018-9-11 end_date_string = 2018-10-11
def get_date_between_days(start_date_string, end_date_string):
    date_list = []
    # start_date = datetime.datetime(int(start_date_list[0]), int(start_date_list[1]), int(start_date_list[2]))
    # end_date = datetime.datetime(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2]))
    start_date = change_to_year_month_day_datetime(start_date_string)
    end_date = change_to_year_month_day_datetime(end_date_string)
    print(start_date)
    print(end_date)
    while start_date <= end_date:
        date_list.append(start_date.strftime('%Y-%m-%d'))
        start_date = start_date + datetime.timedelta(1)
    return date_list


def list_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    return ((key, locs) for key, locs in tally.items()
            if len(locs) > 1)


def check_dup(sorted_list):
    name_list = []

    for comment in sorted_list:
        name = comment['name']
        name_list.append(name)
    return name_list


def del_dup(dup_list, sorted_list, save_index):
    print('==========  delete dup ===========')
    for dup in dup_list:
        for i in range(0, len(dup[1])):
            print(dup[1][i])
            temp = dup[1][i]
            print(sorted_list[temp])
            if temp != save_index:
                # print('----------- XXXX delete -------')
                del sorted_list[temp]
                # 删掉一条记录后，下一个index 应该 -1
                if i < len(dup[1]) - 1:
                    # print(dup[1][i+1])
                    dup[1][i + 1] = dup[1][i + 1] - 1
                    # print(dup[1][i+1])
            else:
                print('------------ keep dup index -------')
                print(temp)
                print('-----------------------')
    print('delete dup element success')


# for dup in sorted(list_duplicates(source)):
#     print(dup)

# def write_excel(rb, row, col, str):
#     # file = 'test.xlsx'
#     # rb = xlrd.open_workbook(file)
#     wb = copy(rb)
#     ws = wb.get_sheet(0)
#     ws.write(row, col, str)
#     return wb
#     # wb.save(file)

def get_excel_max_rows_cols(file, sheet_index):
    data = xlrd.open_workbook(file, formatting_info=True)
    # able = data.sheets()[0]  # 通过索引顺序获取

    table = data.sheet_by_index(sheet_index)  # 通过索引顺序获取 　　
    row_count = table.nrows

    col_count = table.ncols
    return row_count, col_count


def search_excel_row_col(file, sheet_index, keyword):
    # file = 'test.xlsx'
    data = xlrd.open_workbook(file, formatting_info=True)
    # able = data.sheets()[0]  # 通过索引顺序获取

    table = data.sheet_by_index(sheet_index)  # 通过索引顺序获取 　　
    row_count = table.nrows

    col_count = table.ncols
    # row_count =  rb.# 行数
    # col_count = ws # 列数
    # print(row_count)
    # print(col_count)
    #  搜索关键字符串
    # KeyStr = '2018-10-19'
    # keywork = '小诙侠'
    # print('============================== go to search =================================')
    search_row = 'false'
    search_col = 'false'
    for row in range(row_count):
        if str(keyword) in (str(table.row_values(row))):
            # print("*************************************************************************************************")
            # print(row)
            # print(keyword)
            search_row = str(row)

    for col in range(col_count):
        if str(keyword) in (str(table.col_values(col))):
            # print("*************************************************************************************************")
            # print(col)
            # print(keyword)
            search_col = str(col)

    return search_row, search_col


# file = 'test.xlsx'
# print(search_excel_row_col(file, 'abc'))
def init_excel_by_input_date(file, start_date_string, end_date_string):
    rb = xlrd.open_workbook(file)
    wb = copy(rb)
    ws = wb.get_sheet(0)

    ws.write(0, 0, 'id')
    ws.write(0, 1, 'name')

    date_list = get_date_between_days(start_date_string, end_date_string)
    print(date_list)
    date_list.append('count')

    for i in range(len(date_list)):
        # ws = wb.get_sheet(0)
        ws.write(0, i + 2, date_list[i])
    wb.save(file)
    print('init excel success...')


def init_excel(file, sheet_index, month):
    # file = 'test.xlsx'
    rb = xlrd.open_workbook(file)
    wb = copy(rb)
    ws = wb.get_sheet(sheet_index)

    ws.write(0, 0, 'id')
    ws.write(0, 1, 'name')

    date_list = []
    mdays = calendar.mdays
    if month < 10:
        month_string = '0' + str(month)
    else:
        month_string = str(month)

    if month + 1 < 10:
        next_month_string = '0' + str(month + 1)
    else:
        next_month_string = str(month + 1)

    for i in range(mdays[month]):
        if i + 25 <= mdays[month]:
            date_string = '2018-' + str(month_string) + '-' + str(i + 25)
            date_list.append(date_string)

    for i in range(24):
        if i + 1 < 10:
            date_string = '2018-' + next_month_string + '-0' + str(i + 1)
        else:
            date_string = '2018-' + next_month_string + '-' + str(i + 1)
        date_list.append(date_string)
    print(date_list)
    date_list.append('count')

    for i in range(len(date_list)):
        # ws = wb.get_sheet(0)
        ws.write(0, i + 2, date_list[i])
    wb.save(file)
    print('init excel success...')


def create_excel():
    # 创建工作簿
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建工作表
    wbk.add_sheet('9-10', cell_overwrite_ok=True)
    wbk.add_sheet('10-11', cell_overwrite_ok=True)
    wbk.add_sheet('11-12', cell_overwrite_ok=True)
    excel = r"qun_comments_data_new.xls"
    # excel = r"qun_comments_data_new.xlsx"
    wbk.save(excel)
    print('create the excel and add sheets...')
    return excel


def create_excel_by_automation():
    # 创建工作簿
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建工作表
    wbk.add_sheet('comments', cell_overwrite_ok=True)
    excel = r"qun_comments_data_automation.xls"
    # excel = r"qun_comments_data_new.xlsx"
    wbk.save(excel)
    print('create the excel and add sheets...')
    return excel

#
# file = create_excel()
# file = 'qun_comments_data_new.xls'
# # file = 'qun_comments_data_new.xlsx'
# init_excel(file, 1, 10)

# file = 'test.xlsx'
# init_excel(0)
# excel_max_rows_cols = get_excel_max_rows_cols(file, 0)
# print(excel_max_rows_cols)

# print(get_date(26))
