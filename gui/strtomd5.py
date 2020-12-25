import hashlib
import wx


def str_trans_to_md5(event):
    comm = input_text.GetValue().strip().replace("\n", "").encode()
    # print(comm)
    if comm:
        try:
            myMd5 = hashlib.md5()
            myMd5.update(comm)
            myMd5_Digest = myMd5.hexdigest()
            # print(myMd5_Digest)
            # 输出到界面
            output_text.Clear()
            output_text.AppendText(myMd5_Digest)
        except:
            output_text.Clear()
            output_text.AppendText("加密失败!")
    else:
        output_text.Clear()
        output_text.AppendText("不能传入空字符串!")


def selectAll(event):
    # print(event.GetKeyCode())
    if event.GetKeyCode() == 65 and event.ControlDown():
        input_text.SelectAll()


def onCopy(event):
    text_obj = wx.TextDataObject()
    text_obj.SetText(output_text.GetValue())
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        wx.TheClipboard.SetData(text_obj)
        wx.TheClipboard.Close()


app = wx.App()
frame = wx.Frame(None, title="MD5加密工具", size=(800, 600))
panel = wx.Panel(frame)

# label1 = wx.StaticText(panel, -1, u'待加密字符串: ', pos=(0, 50), size=(80, 30), style=wx.ALIGN_RIGHT)
label1 = wx.StaticText(panel, -1, u'待加密字符串: ', size=(80, 30), style=wx.ALIGN_RIGHT)
label2 = wx.StaticText(panel, -1, u'加密字符串: ', size=(80, 30), style=wx.ALIGN_RIGHT)
input_text = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE)
input_text.SetInsertionPoint(0)
output_text = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE)
output_text.SetInsertionPoint(0)

# 按钮
trans_button = wx.Button(panel, label='加密')
clear_button = wx.Button(panel, label='清空加密')
verify_button = wx.Button(panel, label='解密校验')
copy_button = wx.Button(panel, label='复制结果')

# 绑定事件
input_text.Bind(wx.EVT_KEY_UP, selectAll)
trans_button.Bind(wx.EVT_BUTTON, str_trans_to_md5)
copy_button.Bind(wx.EVT_BUTTON, onCopy)

hbox1 = wx.BoxSizer()
hbox1.Add(label1, 0)
hbox1.Add(input_text, 1, wx.EXPAND | wx.LEFT, 5)
vbox1 = wx.BoxSizer(wx.VERTICAL)
vbox1.Add(trans_button)
vbox1.Add(clear_button, 0,  wx.TOP, 20)
hbox1.Add(vbox1, 0, wx.LEFT, 5)

hbox2 = wx.BoxSizer()
hbox2.Add(label2, 0)
hbox2.Add(output_text, 1, wx.EXPAND | wx.LEFT, 5)
vbox2 = wx.BoxSizer(wx.VERTICAL)
vbox2.Add(verify_button)
vbox2.Add(copy_button, 0, wx.TOP, 20)
hbox2.Add(vbox2, 0, wx.LEFT, 5)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox1, 1, wx.EXPAND | wx.ALL, 5)
vbox.Add(hbox2, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 5)

panel.SetSizer(vbox)

frame.Show()
app.MainLoop()
