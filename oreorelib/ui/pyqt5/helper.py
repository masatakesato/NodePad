from PyQt5.QtCore import QMetaMethod
from PyQt5.QtCore import QObject



def getSignal (oObject : QObject, strSignalName : str):
    oMetaObj = oObject.metaObject()
    for i in range (oMetaObj.methodCount()):
        oMetaMethod = oMetaObj.method(i)
        if not oMetaMethod.isValid():
            continue
        if oMetaMethod.methodType () == QMetaMethod.Signal and \
            oMetaMethod.name() == strSignalName:
            return oMetaMethod

    return None