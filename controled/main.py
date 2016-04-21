# -*-coding:utf8-*-
from mailHelper import mailHelper
from analysisDocument import document
from win32 import *
from zipfiles import zipFile
from configReader import configReader
from ctrLog import *
import time
class MCC(object):
    CONFIGPATH = '_config.ini'

    def __init__(self,ctrlog):
        self.ctrLog = ctrlog
        cfReader = configReader(self.CONFIGPATH)
        self.mailHelper=mailHelper(self.ctrLog)
        self.bossMail = cfReader.readConfig('Boss', 'mail')
        self.cmdDic=self.getcmd()

    def getcmd(self):
        self.ctrLog.ctrWriteLog(u'开始获取命令')
        print u'开始获取命令'
        try:
            mailinfo = self.mailHelper.getMailnfo()
            cmddic ={}
            cmddic["type"]=mailinfo['Subject']
            cmddic["cmd"]=mailinfo["Content"]
            cmddic["from"]=mailinfo["From"]
            self.ctrLog.ctrWriteLog(u'获取命令成功')
            print u'获取命令成功'
            return cmddic
        except Exception,e:
             self.ctrLog.ctrError(u'获取命令失败'+str(e))
             print u'获取命令失败'
             return None


    def analyscmd(self):
        cmddic=self.cmdDic
        self.ctrLog.ctrWriteLog(u'开始解析命令 :'+str(cmddic))
        print u'开始解析命令 :'+str(cmddic)
        if cmddic["from"]==self.bossMail:
            self.ctrLog.ctrWriteLog(u'开始获取命令类型 :'+cmddic["type"])
            print u'开始获取命令类型 :'+cmddic["type"]
            if str(cmddic["type"]).lower()=="open":
                try:
                    path=cmddic["cmd"].decode("gbk")
                    self.ctrLog.ctrWriteLog(u'开始打开文件 :'+path)
                    print u'开始打开文件 :'+path
                    doc=document(path)
                    if doc.run()==None:
                        sendinfo="success"
                    else:
                        filelist=doc.run()
                        sendinfo=''
                        for file in filelist:
                            doc=document(path+'/'+file)
                            sendinfo+=doc.getinfo()
                    self.mailHelper.sendMail("Boss",content=sendinfo)
                    self.ctrLog.ctrWriteLog(cmddic["type"]+"  "+cmddic["cmd"].decode("gbk")+u'  命令执行成功！')
                    print cmddic["type"]+"  "+cmddic["cmd"].decode("gbk")+u'  命令执行成功！'
                except Exception, e:
                    self.ctrLog.ctrError(cmddic["type"]+"  "+cmddic["cmd"].decode("gbk")+u'  命令执行失败！'+str(e))
            elif str(cmddic["type"]).lower()=="exit":
                self.ctrLog.ctrWriteLog(u'退出程序')
                print "exit"
                return "exit"
            elif str(cmddic["type"]).lower()=="get":
                self.ctrLog.ctrWriteLog(u'开始获取文件 :'+cmddic["cmd"])
                print u'开始获取文件 :'+cmddic["cmd"]
                try:
                    path=cmddic["cmd"]
                    if document(path).isfile:
                        self.mailHelper.sendMail("Boss",content=u"get",attchamentpath=path)
                    else:
                        zipFile(path)
                        self.mailHelper.sendMail("Boss",content=u"get",attchamentpath="D:/my.zip")
                    self.ctrLog.ctrWriteLog(u'文件获取成功！')
                    print u'文件获取成功！'
                except Exception, e:
                    self.ctrLog.ctrError(u'文件获取失败！'+str(e))
                    print u'文件获取失败！'
            elif str(cmddic["type"]).lower()=="msgbox":
                try:
                     content=cmddic["cmd"]
                     msgbox(content)
                     self.ctrLog.ctrWriteLog(cmddic["type"]+u'操作成功！')
                     print cmddic["type"]+u'操作成功！'
                except Exception, e:
                    self.ctrLog.ctrError(cmddic["type"]+u'操作失败！'+str(e))
                    print cmddic["type"]+u'操作失败！'
            return "ok"
        else:
            self.ctrLog.ctrWriteLog(u'不是指定邮箱操作')
            print u'不是指定邮箱操作'
            return None


if __name__ == "__main__":
    ctrLog=ctrLog()
    fisrtmcc=MCC(ctrLog)
    fisrtmcc.mailHelper.sendMail("Slave",content="begin")
    lastcmd=" "
    fisrtmcc.ctrLog.ctrWriteLog(u'开始运行\n')
    print u'开始运行'
    time.sleep(10)
    while True:
        mcc=MCC(ctrLog)
        recentcmd=mcc.cmdDic
        print "getcmd  ",
        print recentcmd
        if recentcmd==lastcmd:
            print u'没有获取到新的指令'
            mcc.ctrLog.ctrWriteLog(u'没有获取到新的指令')
            mcc.ctrLog.ctrWriteLog(u'next\n')
            time.sleep(5)
            continue
        mcc.ctrLog.ctrWriteLog(u'获取到新的指令')
        print u'获取到新的指令'
        lastcmd=recentcmd
        rtn=mcc.analyscmd()
        print "ok"
        if rtn=="exit":
            break
        time.sleep(10)
        mcc.ctrLog.ctrWriteLog(u'next\n')
        print '\n'
    exit()