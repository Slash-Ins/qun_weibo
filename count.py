

from xlutils.copy import copy
import xlrd
from tools import search_excel_row_col


def count_daka(file, sheet_index):
    data = xlrd.open_workbook(file)
    table = data.sheets()[sheet_index]

    list_user_count = []
    for i in range(table.nrows):
        if i == 0:
            continue
        temp_record = {}
        temp_count = 0
        temp_row = table.row_values(i)
        print('------- num row -----------')
        print(i)
        print(temp_row)
        for k in range(len(temp_row)):
            if str(temp_row[k]) == '1':
                temp_count = temp_count + 1
            temp_record = {'name': temp_row[1], 'count': temp_count}

        list_user_count.append(temp_record)
    print('------------ user daka record ----------')
    print(list_user_count)

    # file = 'qun_comments_data_new.xlsx'
    count_excel = search_excel_row_col(file,sheet_index, str('count'))

    rb = xlrd.open_workbook(file)
    wb = copy(rb)
    ws = wb.get_sheet(sheet_index)

    for record in list_user_count:
        temp_name = search_excel_row_col(file, sheet_index,record['name'])
        # print('---------------- name -----------------')
        # print(temp_name[0])
        # print(temp_name[1])
        # print('---------------- count --------------')
        # print(count_excel[1])
        # print(record['count'])
        ws.write(int(temp_name[0]), int(count_excel[1]), str(record['count']))

    wb.save(file)

# file = 'qun_comments_data_new.xlsx'
# count_daka(file, 0)