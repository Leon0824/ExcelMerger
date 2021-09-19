import wx

class HelloFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(HelloFrame, self).__init__(*args, **kw)

        pnl: wx.Panel = wx.Panel(self)
        st: wx.StaticText = wx.StaticText(pnl, label="Hello World!")
        font: wx.Font = st.GetFont()
        font.PointSize += 10
        font: wx.Font = font.Bold()
        st.SetFont(font)

        sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        pnl.SetSizer(sizer)

if __name__ == '__main__':
    app: wx.App = wx.App()
    frm: HelloFrame = HelloFrame(None, title='Hello World', size=(400,400))
    frm.Show()
    app.MainLoop()
