import subprocess
import wx
import xlrd


def file_content(filename, sheet_name):
    table = xlrd.open_workbook(filename)
    sheet_content = table.sheet_by_name(sheet_name)
    row_num = sheet_content.nrows
    title_content = sheet_content.row_values(0)
    result = []
    for i in range(1, row_num):
        result.append(dict(zip(title_content, sheet_content.row_values(i))))
    return result


temp_file, name_link_dict, button_list, event_list = file_content("IP_link.xlsx", "Ip"), {}, [], []
for i in temp_file:
    name_link_dict.update({i['Name']: i['Link']})
name_list = sorted(name_link_dict.keys())
app = wx.App()
frame = wx.Frame(None, title="FolderHelper", size=(250, 400))
scroll, vbox = wx.ScrolledWindow(frame, -1), wx.BoxSizer(wx.VERTICAL)
scroll.SetScrollbars(1, 1, 250, 400)
for i in range(len(name_list)):
    button_list.append(wx.Button(scroll, label=name_list[i], pos=(0, 25 + 25 * i)))
for i in range(len(name_list)):
    vbox.Add(button_list[i], 0, wx.EXPAND | wx.ALIGN_CENTER)
for i in range(len(name_list)):
    event_list.append(lambda event, comm=name_link_dict[name_list[i]]: subprocess.run(r'''start "" '''+'''"'''+comm+'''"''', shell=True))
for i in range(len(name_list)):
    event_list[i].Bind(wx.EVT_BUTTON, event_list[i], button_list[i])
scroll.SetSizer(vbox)
frame.Show()
app.MainLoop()

