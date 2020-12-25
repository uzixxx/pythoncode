import wx

app = wx.App()
frame = wx.Frame(None, title="MD5加密工具", size=(800, 600))
panel = wx.Panel(frame)

label1 = wx.StaticText(panel, -1, u'待加密字符串: ', pos=(0, 50), size=(80, 30), style=wx.ALIGN_RIGHT)

frame.Show()
app.MainLoop()
