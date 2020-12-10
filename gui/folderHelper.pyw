#coding:utf-8
import os,xlrd,wx,subprocess
def FileContent(filename, sheetname):
    table = xlrd.open_workbook(filename)
    sheetcontent = table.sheet_by_name(sheetname)
    colesNum = sheetcontent.nrows
    titlecontent = sheetcontent.row_values(0)
    result=[]
    for _ in map(lambda i:result.append(dict(zip(titlecontent, sheetcontent.row_values(i)))),range(1,colesNum)):pass
    return result
tempFile,IP_File_HASH,BUTTON_LIST,EVENT_LSIT=FileContent( "IP_link.xlsx", "Ip"),{},[],[]
for _ in map(lambda i:IP_File_HASH.update({i['Name']:i['Link']}),tempFile):pass
IP_NAME_LIST=sorted(IP_File_HASH.keys())
app = wx.App()
frame = wx.Frame(None,title="YOU ARE HANDSOME",size=(200,400))
scroll,vbox = wx.ScrolledWindow(frame, -1),wx.BoxSizer(wx.VERTICAL)
scroll.SetScrollbars(1, 1, 200, 400)
for _ in map(lambda i:BUTTON_LIST.append(wx.Button(scroll, label=IP_NAME_LIST[i], pos=(0, 25 + 25 * i))),range(len(IP_NAME_LIST))):pass
for _ in map(lambda i:vbox.Add(BUTTON_LIST[i], 0, wx.EXPAND | wx.ALIGN_CENTER),range(len(IP_NAME_LIST))):pass
for _ in map(lambda i:EVENT_LSIT.append(lambda event,comm=IP_File_HASH[IP_NAME_LIST[i]]:subprocess.run(r'''start "" '''+'''"'''+comm+'''"''', shell=True)),range(len(IP_NAME_LIST))):pass
for _ in map(lambda i:BUTTON_LIST[i].Bind(wx.EVT_BUTTON,EVENT_LSIT[i],BUTTON_LIST[i]),range(len(IP_NAME_LIST))):pass
scroll.SetSizer(vbox)
frame.Show()
app.MainLoop()