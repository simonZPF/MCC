# -*-coding:utf8-*-
import os
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
class document(object):
    def __init__(self,path):
        self.path=path.encode("gbk")
        self.attr=os.stat(self.path)
        self.isfile=os.path.isfile(self.path)
        self.isdir=os.path.isdir(self.path)

    def getSize(self):
        if self.isfile:
            size=self.attr.st_size
            if size<1024:
                return str(size)+"B"
            elif size<1024**2:
                return str(size/1024)+"KB"
            elif size<1024**3:
                return str(size/(1024**2))+"MB"
            else:
                return str(size/(1024**3))+"GB"
        else:
            return "   "

    def getdate(self,timeAttr="ctime"):
        timeAttrDir={"ctime":self.attr.st_ctime,    #创建时间
                     "atime":self.attr.st_atime,    #最后访问时间
                     "mtime":self.attr.st_mtime}    #最后修改时间
        t=time.localtime(timeAttrDir[timeAttr])
        return str(time.strftime(u"%Y-%m-%d %A %X", t))

    def getinfo(self):
        fileinfo=os.path.basename(self.path).decode("gbk")
        fileinfo+="   "+self.getSize()+"   "+self.getdate()+" \r\n"
        return fileinfo

    def run(self):
        if self.isfile:
            try:
                os.system(self.path)
                return None
            except Exception,e:
                pass
        elif self.isdir:
            filelist=os.listdir(self.path)
            return filelist
        else:
            pass

