#-*-coding:utf8-*-
import wx
from mailHelper import mailHelper
from ctrLog import *
from mainFrame import mainFrame
class logFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=u'登陆', size=(200, 350))
        self.ctrLog=ctrLog()

        self.panel = wx.Panel(self, -1)
        self.Centre()

        self.nameStatic = wx.StaticText(self.panel, -1, u'账号： ')
        self.passStatic = wx.StaticText(self.panel, -1, u'密码： ')

        self.nameText=wx.TextCtrl(self.panel,-1,u"",size=(180,20))
        self.passText=wx.TextCtrl(self.panel,-1,u"",style=wx.TE_PASSWORD,size=(180,20))

        self.logBtn=wx.Button(self.panel,label=u"登陆")
        self.Bind(wx.EVT_BUTTON, self.log, self.logBtn)

        self.gridBagSizerAll = wx.GridBagSizer(hgap=5, vgap=5)
        self.gridBagSizerAll.Add(self.nameStatic,pos=(0, 0),flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.gridBagSizerAll.Add(self.passStatic,pos=(2, 0),flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.gridBagSizerAll.Add(self.nameText,pos=(0, 1),span=(1,3),flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.gridBagSizerAll.Add(self.passText,pos=(2, 1),span=(1,2),flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.gridBagSizerAll.Add(self.logBtn,pos=(4,1),flag=wx.ALIGN_CENTER_VERTICAL, border=5)
        self.panel.SetSizer(self.gridBagSizerAll)
        self.gridBagSizerAll.Fit(self)
        self.ctrLog.ctrWriteLog(u'进入登陆界面')
    def log(self,event):
        username=self.nameText.GetValue()
        password=self.passText.GetValue()
        self.ctrLog.ctrWriteLog(u'请求登陆')
        try:
            mail=mailHelper(self.ctrLog,username,password)
            if mail.ok:
                self.Destroy()
                frame=mainFrame(mail,self.ctrLog)
                frame.Show()
                event.Skip()
                print u"登陆成功~~"
                self.ctrLog.ctrWriteLog(u'username:  '+username.encode("utf8")
                                        +u'\npassword:  '+password.encode("utf8")+
                                        u"   登陆成功！")
            else:
                wx.MessageBox(u"登陆失败 !", u"wrong" ,wx.OK | wx.ICON_INFORMATION)
                self.ctrLog.ctrError(u'username:  '+username.encode("utf8")
                                        +u'password:  '+password.encode("utf8")+
                                        u"  登陆失败！")
        except Exception,e:
            print u"登陆出现错误"+str(e)
            self.ctrLog.ctrError(u"登陆出现错误！")

if __name__=="__main__":
    app=wx.App()
    frame=logFrame()
    frame.Show()
    app.MainLoop()