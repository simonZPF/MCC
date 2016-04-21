# -*-coding:utf8-*-

from email.parser import Parser
import poplib
import smtplib
import sys
from configReader import configReader
from createMail import *
reload(sys)
sys.setdefaultencoding('utf-8')
class mailHelper(object):
    CONFIGPATH = '_config.ini'

    def __init__(self,ctrlog,username='',password=''):
        self.ctrLog = ctrlog
        cfReader = configReader(self.CONFIGPATH)
        self.pophost = cfReader.readConfig('Slave', 'pophost')
        self.smtphost = cfReader.readConfig('Slave', 'smtphost')
        self.port = cfReader.readConfig('Slave', 'port')
        self.username = username
        self.password = password
        self.ok=False
        self.loginMail()
        self.configSlaveMail()


    def loginMail(self):
        self.ctrLog.ctrWriteLog(u'开始登录邮箱')
        print u'开始登录邮箱'
        try:
            self.pp = poplib.POP3_SSL(self.pophost)
            self.pp.set_debuglevel(0)
            self.pp.user(self.username)
            self.pp.pass_(self.password)
            self.pp.list()
            print u'登录成功！'
            self.ctrLog.ctrWriteLog(u'登录邮箱成功。')
        except Exception,e:
            print u'登录失败！'
            self.ctrLog.ctrError(u'登录邮箱失败' + str(e))


    def configSlaveMail(self):
        self.ctrLog.ctrWriteLog(u'开始配置发件箱。')
        print u'开始配置发件箱。'
        try:
            self.handle = smtplib.SMTP(self.smtphost, self.port)
            self.handle.login(self.username, self.password)
            self.ctrLog.ctrWriteLog(u'发件箱配置成功')
            print u'发件箱配置成功'
            self.ok=True
        except Exception, e:
            self.ctrLog.ctrError(u'发件箱配置失败' + str(e))
            print u'发件箱配置失败'


    def sendMail(self,receiver,subject="OK", content='Success',attchamentpath='no'):
        mail={}
        mail['Subject'] = subject
        mail['From'] = self.username
        mail["Content"]=content
        mail["To"]=receiver
        if attchamentpath=='no':
            msg = createMsg(mail)
        else:
            msg = createMsg(mail,path=attchamentpath,attchament=True)
        self.ctrLog.ctrWriteLog(u'开始发送邮件'+ 'to: ' + receiver)
        print u'开始发送邮件'+ 'to: ' + receiver
        try:
            self.handle.sendmail(self.username,receiver, msg.as_string())
            self.ctrLog.ctrWriteLog(u'发送邮件成功')
            print u'发送邮件成功'
            return True
        except Exception,e:
            self.ctrLog.ctrError(u'发送邮件失败' + str(e))
            print u'发送邮件失败'
            return False