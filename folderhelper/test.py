import subprocess
import wx
import xlrd


def file_content(filename, sheet_name):
    table = xlrd.open_workbook(filename)
    sheet_content = table.sheet_by_name(sheet_name)
    row_nums = sheet_content.nrows
    title_content = sheet_content.row_values(0)
    result = []
    for row_num in range(1, row_nums):
        result.append(dict(zip(title_content, sheet_content.row_values(row_num))))
    return result


temp_file = file_content("test.xlsx", "Link")
name_link = {}
button_list = []
event_list = []
for i in temp_file:
    name_link.update({i['Name']: i['Link']})
name_list = sorted(name_link.keys())
app = wx.App()
frame = wx.Frame(None, title="FolderHelper", size=(250, 400))
scroll = wx.ScrolledWindow(frame, -1)
vbox = wx.BoxSizer(wx.VERTICAL)
scroll.SetScrollbars(1, 1, 250, 400)
for i in range(len(name_list)):
    button_list.append(wx.Button(scroll, label=name_list[i], pos=(0, 25 + 25 * i)))
for i in range(len(name_list)):
    vbox.Add(button_list[i], 0, wx.EXPAND | wx.ALIGN_CENTER)
for i in range(len(name_list)):
    event_list.append(lambda event, comm=name_link[name_list[i]]: subprocess.run(r'''start "" '''+'''"'''+comm+'''"''',
                                                                                 shell=True))
for i in range(len(name_list)):
    button_list[i].Bind(wx.EVT_BUTTON, event_list[i], button_list[i])
scroll.SetSizer(vbox)
frame.Show()
app.MainLoop()

