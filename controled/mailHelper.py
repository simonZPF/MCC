# -*-coding:utf8-*-

from email.parser import Parser
import poplib
import smtplib
import sys
from configReader import configReader
from createMail import *
from analysisMail import *
reload(sys)
sys.setdefaultencoding('utf-8')
class mailHelper(object):
    CONFIGPATH = '_config.ini'

    def __init__(self,ctrlog=None):
        self.ctrLog = ctrlog
        cfReader = configReader(self.CONFIGPATH)
        self.pophost = cfReader.readConfig('Slave', 'pophost')
        self.smtphost = cfReader.readConfig('Slave', 'smtphost')
        self.port = cfReader.readConfig('Slave', 'port')
        self.username = cfReader.readConfig('Slave', 'username')
        self.password = cfReader.readConfig('Slave', 'password')
        self.bossMail = cfReader.readConfig('Boss', 'mail')
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
            exit()

    def analysisMail(self, msg):
        self.ctrLog.ctrWriteLog(u'开始解析邮件内容')
        print u'开始解析邮件内容'
        try:
            self.ctrLog.ctrWriteLog(u'解析成功')
            print u'解析成功'
            return analysisMsg(msg)#信息按字典形式返回
        except Exception, e:
            self.ctrLog.ctrError(u'解析失败' + str(e))
            print u'解析失败'
            return None

    def configSlaveMail(self):
        self.ctrLog.ctrWriteLog(u'开始配置发件箱。')
        print u'开始配置发件箱。'
        try:
            self.handle = smtplib.SMTP(self.smtphost, self.port)
            self.handle.login(self.username, self.password)
            self.ctrLog.ctrWriteLog(u'发件箱配置成功')
            print u'发件箱配置成功'
        except Exception, e:
            self.ctrLog.ctrError(u'发件箱配置失败' + str(e))
            print u'发件箱配置失败'
            exit()

    def acceptMail(self):
        self.ctrLog.ctrWriteLog(u'开始抓取邮件。')
        print u'开始抓取邮件。'
        try:
            resp, mails, octets = self.pp.list()# 获取最新一封邮件, 注意索引号从1开始:
            index = len(mails)
            resp, lines, octets = self.pp.retr(index)# lines存储了邮件的原始文本的每一行,
            msg_content = '\r\n'.join(lines).decode("utf-8")
            msg = Parser().parsestr(msg_content)# 稍后解析出邮件:
            self.ctrLog.ctrWriteLog(u'抓取邮件成功。')
            print u'抓取邮件成功。'
            return msg
        except Exception, e:
            self.ctrLog.ctrError(u'抓取邮件失败' + str(e))
            print u'抓取邮件失败'
            return None

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
        self.ctrLog.ctrWriteLog(u'开始发送邮件'+ 'to' + receiver)
        print u'开始发送邮件'+ 'to' + receiver
        if receiver == 'Slave':
            try:
                self.handle.sendmail(self.username, self.username, msg.as_string())
                self.ctrLog.ctrWriteLog(u'发送邮件成功')
                print u'发送邮件成功'
                return True
            except Exception,e:
                self.ctrLog.ctrError(u'发送邮件失败' + str(e))
                print u'发送邮件失败'
                return False

        elif receiver == 'Boss':
            try:
                self.handle.sendmail(self.username, self.bossMail, msg.as_string())
                self.ctrLog.ctrWriteLog(u'发送邮件成功')
                print u'发送邮件成功'
            except Exception,e:
                self.ctrLog.ctrError(u'发送邮件失败' + str(e))
                print u'发送邮件失败'
                return False

    def getMailnfo(self):
            msg=self.acceptMail()
            msgdic=self.analysisMail(msg)
            return msgdic