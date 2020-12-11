import subprocess
import wx
import xlrd


def FileContent(filename, sheetname):
    table = xlrd.open_workbook(filename)
    sheetcontent = table.sheet_by_name(sheetname)
    colesNum = sheetcontent.nrows
    titlecontent = sheetcontent.row_values(0)
    result = []
    for i in range(1, colesNum):
        result.append(dict(zip(titlecontent, sheetcontent.row_values(i))))
    return result


tempFile, IP_File_HASH, BUTTON_LIST, EVENT_LSIT = FileContent("IP_link.xlsx", "Ip"), {}, [], []
for i in tempFile:
    IP_File_HASH.update({i['Name']: i['Link']})
IP_NAME_LIST = sorted(IP_File_HASH.keys())
app = wx.App()
frame = wx.Frame(None, title="FolderHelper", size=(250, 400))
scroll, vbox = wx.ScrolledWindow(frame, -1), wx.BoxSizer(wx.VERTICAL)
scroll.SetScrollbars(1, 1, 250, 400)
for i in range(len(IP_NAME_LIST)):
    BUTTON_LIST.append(wx.Button(scroll, label=IP_NAME_LIST[i], pos=(0, 25 + 25 * i)))
for i in range(len(IP_NAME_LIST)):
    vbox.Add(BUTTON_LIST[i], 0, wx.EXPAND | wx.ALIGN_CENTER)
for i in range(len(IP_NAME_LIST)):
    EVENT_LSIT.append(lambda event, comm=IP_File_HASH[IP_NAME_LIST[i]]:subprocess.run(r'''start "" '''+'''"'''+comm+'''"''', shell=True))
for i in range(len(IP_NAME_LIST)):
    BUTTON_LIST[i].Bind(wx.EVT_BUTTON, EVENT_LSIT[i], BUTTON_LIST[i])
scroll.SetSizer(vbox)
frame.Show()
app.MainLoop()

