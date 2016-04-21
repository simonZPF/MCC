# -*-coding:utf8-*-
import zipfile
import os

def zipFile(path,filename="D:/my.zip"):


    start = path.rfind(os.sep) + 1
    z = zipfile.ZipFile(filename,"w",zipfile.ZIP_DEFLATED)
    try:
        for dirpath,dirs,files in os.walk(path):
            for file in files:
                if file == filename or file == "zip.py":
                    continue
                z_path = os.path.join(dirpath,file)
                z.write(z_path,z_path[start:])
        z.close()
    except:
        if z:
            z.close()
