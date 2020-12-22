import xlrd

filename = 'folder_link.xlsx'
xl = xlrd.open_workbook(filename)


print(xl.sheet_names())  # 返回book中所有工作表的名字以列表的形式
table = xl.sheets()[0]  # 通过索引顺序获取工作表
# table = xl.sheet_by_index(0)  # 通过索引顺序获取工作表
# table = xl.sheet_by_name('Link')  # 通过名称获取工作表


nrows = table.nrows  # 获取该sheet中的有效行数
print(table.row_values(0))  # 返回行对象以列表的形式
print(table.row_values(1))
print(list(zip(table.row_values(0), table.row_values(1))))
print(dict(zip(table.row_values(0), table.row_values(1))))
