import wx


def load(event):
    file = open(filename.GetValue())
    contents.SetValue(file.read())
    file.close()


def save(event):
    file = open(filename.GetValue(), 'w')
    file.write(contents.GetValue())
    file.close()


app = wx.App()
win = wx.Frame(None, title="编辑器", size=(410, 335))
bkg = wx.Panel(win)

loadButton = wx.Button(bkg, label='打开')
loadButton.Bind(wx.EVT_BUTTON, load)

saveButton = wx.Button(bkg, label='保存')
saveButton.Bind(wx.EVT_BUTTON, save)

filename = wx.TextCtrl(bkg)
contents = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)

hbox = wx.BoxSizer()  # 默认为水平
hbox.Add(filename, proportion=1, flag=wx.EXPAND)
hbox.Add(loadButton, proportion=0, flag=wx.LEFT, border=5)
hbox.Add(saveButton, proportion=0, flag=wx.LEFT, border=5)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(contents, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 5)

bkg.SetSizer(vbox)


win.Show()
app.MainLoop()
