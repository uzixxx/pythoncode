import wx
import subprocess


def callback(event, comm='hello'):
    print(comm)


app = wx.App()
frame = wx.Frame(None, title="FolderHelper", size=(250, 400))
scroll = wx.ScrolledWindow(frame, -1)
scroll.SetScrollbars(1, 1, 250, 400)
vbox = wx.BoxSizer(wx.VERTICAL)

button1 = wx.Button(scroll, label='button1')
button1.Bind(wx.EVT_BUTTON, callback)
vbox.Add(button1, 0, wx.EXPAND | wx.ALIGN_CENTER)

scroll.SetSizer(vbox)
frame.Show()
app.MainLoop()
