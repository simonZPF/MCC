#-*-coding:utf8-*-
import win32api
import win32con
def msgbox(content,title="hello"):
    win32api.MessageBox(win32con.NULL, content, title, win32con.MB_OK)