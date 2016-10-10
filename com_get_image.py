import win32com.client
import time
import datetime
import md5
from PyQt4.QtCore import *
from PyQt4.QtGui import *


def produceData():
    now = datetime.datetime.now()
    a = str(now.year) + str(now.strftime('%m')) + str(now.strftime('%d'))

    GeODin = win32com.client.Dispatch("GeODin.GeODinApplication")
    info = GeODin.LicenceInfo.split('\r\n')
    dongle = [t for t in info if 'Dongle' in t][0].split(': ')[1]
    m = md5.new(a+'-'+dongle)
    new_hash = m.hexdigest()

    params = "[Params]\nEXECUTE=ProducePortalImage\nLAYOUT={0}\nPageNumber=1\nScale=0\nVersionName=\nArcGeODin={1}\n[Database]\nName={2}\nUsername= \nPassword= \n[Objects]\nObjectID1={3}\n[Image]\nImageType=21\nResolution=0".format("G:\GeODin\Demos\Berlin\Layouts_Maps\Anionen-Bericht.GLO", new_hash, "Berlin", "WYYYL40002BRG000")

    pic = GeODin.ProduceData(params)
    if GeODin.ExceptionValue != 0: 
        print "Error ID:"+ str(GeODin.ExceptionValue)
        print "Error Message:"+GeODin.ExceptionMsg

    time.sleep(3)

    f = open(r'C:\Users\phielerm\out.png', 'wb')
    f.write(pic[0])
    f.close()

    GeODin = None

    img = QImage(str(pic[0]), 500, 500)

    return pic

produceData()
