import subprocess
import wx
import xlrd


def file_content(filename, sheet_name):
    xl = xlrd.open_workbook(filename)
    table = xl.sheet_by_name(sheet_name)
    nrows = table.nrows
    title = table.row_values(0)
    result = []
    for nrow in range(1, nrows):
        result.append(dict(zip(title, table.row_values(nrow))))
    return result


temp_file = file_content("folder_link.xlsx", "Link")
name_link, button_list, event_list = {}, [], []
for i in temp_file:
    name_link.update({i['Name']: i['Link']})
name_list = sorted(name_link.keys())
app = wx.App()
frame = wx.Frame(None, title="FolderHelper", size=(250, 400))
scroll = wx.ScrolledWindow(frame, -1)
scroll.SetScrollbars(1, 1, 250, 400)
vbox = wx.BoxSizer(wx.VERTICAL)
for i in range(len(name_list)):
    button_list.append(wx.Button(scroll, label=name_list[i]))
for i in range(len(name_list)):
    event_list.append(lambda event, comm=name_link[name_list[i]]: subprocess.run(r'''start "" '''+'''"'''+comm+'''"''',
                                                                                 shell=True))
for i in range(len(name_list)):
    button_list[i].Bind(wx.EVT_BUTTON, event_list[i])
for i in range(len(name_list)):
    vbox.Add(button_list[i], proportion=0, flag=wx.EXPAND | wx.ALIGN_CENTER)
scroll.SetSizer(vbox)
frame.Show()
app.MainLoop()
