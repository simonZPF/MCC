# -*-coding:utf8-*-
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
from email import Encoders
import os
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
def createMsg(mail,attchament=False,path=""):
    if attchament:
        msg = MIMEMultipart()
        msg['From'] = _format_addr(mail["From"])
        msg['To'] = _format_addr(mail["To"])
        msg['Subject'] = Header(mail["Subject"], 'utf-8').encode()
        content=_format_addr(mail["Content"])
        msg.attach(MIMEText(content,"plain","utf-8"))
        with open(path, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            fname =_format_addr(os.path.basename(path))
            mime= MIMEBase('application', 'octet-stream')
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=fname)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            Encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
    else:
        content=mail["Content"]
        msg = MIMEText(content,'plain','utf-8')
        msg['From'] = _format_addr(mail["From"])
        msg['To'] = _format_addr(mail["To"])
        msg['Subject'] = Header(mail["Subject"], 'utf-8').encode()
    return msg