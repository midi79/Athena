from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys

sys.path.append("..")
sys.path.append("../..")

from framework.core.edgecore import Edge

class ViewPort(QLabel):

    def __init__(self, parent=None):
        QLabel.__init__(self,parent)
        self.dataType = None

    def createConnectionLine(self):
        self.core.edge = Edge()
        self.core.edge.setSrcCoord(QPoint(self.pos().x()+self.width()/2,self.pos().y()+self.height()/2) + self.parent.pos())

    def getPos(self):
        return QPoint(self.pos().x()+self.width()/2, self.pos().y()+self.height()/2) + self.parent.pos()

    def setPortCore(self, core):
        self.core = core

    def setPortType(self, dataType):
        self.dataType = dataType

    def checkPosition(self, pos):
        if pos.x() < self.pos().x():
            return False
        if pos.x() > self.pos().x() + self.width():
            return False
        if pos.y() < self.pos().y():
            return False
        if pos.y() > self.pos().y() + self.height():
            return False

        return True

    def getEdge(self):
        return self.core.getEdge()

class Connection(object):

    def setSrcCoord(self, pos):
        self.coordSrc = pos

    def setDstCoord(self, pos):
        self.coordDst = pos

class ViewPortIn(ViewPort):
    
    def __init__(self, parent):
        ViewPort.__init__(self,parent)
        self.connectedTo = None
        self.parent = parent
        self.data = None
        self.setStyleSheet("QLabel { background-color:blue; color:black; border:1px solid white}")

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData(self)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)

    def connectPort(self,portOut):
        self.core.connectPort(portOut.core)

    def disconnectPort(self):
        self.core.disconnectPort()

    def isConnected(self):
        return self.core.isConnected()
      
    def getConnection(self):
        # Connection is created by output port object. So, do not delete on input port.
        # Connection is owned by output port. Request core to get connection info.
        return self.core.getConnection()
     
    def propagateExecution(self):
        if self.connectedTo:
            self.connectedTo.propagateExecution()

    def passToBox(self,data):
        self.data = data

    def getData(self):
        return self.data

    def driveBox(self):
        self.parent.update()        
    
class ViewPortOut(ViewPort):

    def __init__(self,parent):
        ViewPort.__init__(self,parent)
        self.data = None
        self.connection = None
        self.connectedTo = None
        self.parent = parent
        self.setStyleSheet("QLabel {background-color:red; color:black; border:1px solid white}")

    def setData(self, data):
        self.data = data

    def updateDstPosition(self, pos):
        self.core.getEdge().setDstCoord(pos)

    def getConnection(self):
        return self.core.getEdge()

    def deleteConnectionLine(self):
        self.connection = None

    def checkPortMatch(self,portIn):
        if self.dataType == portIn.dataType:
            return True
        else:
            return False

    def isConnected(self):
        return self.core.isConnected()
                    
    def connectPort(self,portIn):
        self.core.connectPort(portIn.core)
        
    def disconnectPort(self):
        self.core.disconnectPort()

    def propagateExecution(self):
        self.parent.run()

    def transferData(self,data):
        if self.connectedTo:
            self.connectedTo.passToBox(data)

    def driveForward(self):
        self.connectedTo.driveBox() 
            
