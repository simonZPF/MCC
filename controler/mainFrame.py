#-*-coding:utf8-*-
import wx
from mailHelper import mailHelper
from ctrLog import *
class mainFrame(wx.Frame):
    def __init__(self,mail,ctrlog=None):
        self.ctrLog=ctrlog
        self.mail=mail
        wx.Frame.__init__(self, parent=None, id=-1, title=u'输入命令', size=(600, 600))
        self.panel = wx.Panel(self, -1)
        self.Centre()

        self.commandStatic = wx.StaticText(self.panel, -1, u'输命令:')
        self.typeStatic = wx.StaticText(self.panel, -1, u'选择命令类型:')

        self.commandText=wx.TextCtrl(self.panel,-1,u"",style=wx.TE_MULTILINE,size=(300,200))

        self.cmdList=[u'打开文件',u'获取文件',u'发送消息框',u'退出']
        self.cmdTypeList=['open','get','msgbox','exit']
        self.cmdChoice=wx.Choice(self.panel, -1, choices=self.cmdList)

        self.clientsList = ['a316829772@sina.com']
        self.clients = wx.ListBox(self.panel, -1, choices=self.clientsList, style=wx.LB_SINGLE)

        self.send = wx.Button(self.panel, label=u'发送命令')
        self.clear = wx.Button(self.panel, label=u'清空命令')
        self.screen = wx.Button(self.panel, label=u'查看屏幕')
        self.Bind(wx.EVT_BUTTON, self.onSend, self.send)
        self.Bind(wx.EVT_BUTTON, self.onClear, self.clear)
        self.Bind(wx.EVT_BUTTON, self.onScreen, self.screen)

        self.img = wx.Image(r'logo.jpg', wx.BITMAP_TYPE_ANY).Scale(400, 400)
        self.screenBox = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.img))

        self.gridBagSizerAll = wx.GridBagSizer(hgap=5, vgap=5)
        self.gridBagSizerAll.Add(self.clients, pos=(0, 0),
                         flag=wx.ALL | wx.EXPAND,
                           span=(7,2),border=5)
        self.gridBagSizerAll.Add(self.commandStatic,pos=(1, 2),flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.gridBagSizerAll.Add(self.typeStatic,pos=(0, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.gridBagSizerAll.Add(self.commandText,pos=(2, 2),span=(4,3),flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,border=5)
        self.gridBagSizerAll.Add(self.cmdChoice,pos=(0, 3),flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.gridBagSizerAll.Add(self.send ,pos=(6, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,border=5)
        self.gridBagSizerAll.Add(self.clear,pos=(6, 4) ,flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,border=5)
        self.gridBagSizerAll.Add(self.screen,pos=(0, 4),flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.gridBagSizerAll.Add(self.screenBox,pos=(0, 5),span=(7,6),flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.panel.SetSizer(self.gridBagSizerAll)
        self.gridBagSizerAll.Fit(self)
        self.ctrLog.ctrWriteLog(u'进入控制台')

    def onScreen(self, event):
        img = wx.Image(r'python.jpg', wx.BITMAP_TYPE_ANY).Scale(400, 400)
        self.screenBox.SetBitmap(wx.BitmapFromImage(img))
        self.gridBagSizerAll.Fit(self)

    def onClear(self, event):
        self.commandText.Clear()
        self.commandText.AppendText(u'')
        self.ctrLog.ctrWriteLog(u'清空命令文字')

    def _onSend(self, event):
        if self.clients.GetSelection() != -1:
            client = self.clientsList[self.clients.GetSelection()]
        else:
            client = None
        if self.cmdChoice.GetSelection()!=-1:
            cmdType=self.cmdTypeList[self.cmdChoice.GetSelection()]
        else :
            cmdType = None
        command = self.commandText.GetValue().encode("utf8")
        if client==None:
            print u'未选择邮箱！'
            self.ctrLog.ctrError(u'未选择邮箱！')
        elif cmdType==None:
            print u'未选择命令类型！'
            self.ctrLog.ctrError(u'未选择命令类型！')
        else:
            print u'选中的邮箱是： %s' % client
            print u'执行的内置命令是： %s' % cmdType
            print u'写入的Python代码是:\n%s' % command
            self.ctrLog.ctrWriteLog(u'选中邮箱：'+client.encode("utf8"))
            self.ctrLog.ctrWriteLog(u'选中命令类型：'+cmdType.encode("utf8"))
            self.ctrLog.ctrWriteLog(u'命令内容： '+command.encode("utf8"))
            self.mail.sendMail(client,subject=cmdType,content=command)
    def onSend(self, event):
        import thread
        thread.start_new_thread(self._onSend, (event,))

if __name__=="__main__":
    app=wx.App()
    frame=mainFrame()
    frame.Show()
    app.MainLoop()