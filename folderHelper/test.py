import xlrd

filename = 'folder_link.xlsx'
sheet_name = 'Link'
table = xlrd.open_workbook(filename)
sheet_content = table.sheet_by_name(sheet_name)
row_nums = sheet_content.nrows
title_content = sheet_content.row_values(0)
result = []
for row_num in range(1, 3):
    print(title_content)
    print(sheet_content.row_values(row_num))
    result.append(dict(zip(title_content, sheet_content.row_values(row_num))))

print(result)

print('=====\n')
a = {'index': '1', 'Name': 'case01', 'Link': r'D:\360极速浏览器下载'}
b = {'len': '10', 'height': '20'}

print(a.keys())
print(a.values())
print(a.items())

a.update(b)
print(a)

c = {'len': '30'}
a.update(c)
print(a)


