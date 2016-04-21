# -*-coding:utf8-*-
from email.header import decode_header
from email.utils import parseaddr
def analysisMsg(msg):
    msgdic={}
    # 邮件的From, To, Subject存在于根对象上:
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header=='Subject':
                # 需要解码Subject字符串:
                value = decode_str(value)
            else:
                # 需要解码Email地址:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = addr
        msgdic[header]=value
    if (msg.is_multipart()):
        parts=msg.get_payload()
        content=parts[0].get_payload(decode=True)
    else:
        content = msg.get_payload(decode=True)
    # 要检测文本编码:
    charset = guess_charset(msg)
    if charset:
        content = content.decode(charset)
    msgdic["Content"]=content
    return msgdic
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset
