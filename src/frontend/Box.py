from PySide.QtGui import *
from PySide.QtCore import *

import Port

class CommonModuleBox(QFrame):
    
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = '', typeName = ''):
        QFrame.__init__(self, parent)
        self.popupActions = []  # list of dictionary, Key :"title","desc","method"
        self.inPorts = []
        self.outPorts = []
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setContentsMargins(1,1,1,1)
        layout = QVBoxLayout()
        inputLayout = QHBoxLayout()
        inputLayout.addStretch()
        for pin in inputPort:
            new_port = Port.PortIn(self)
            self.inPorts.append(new_port)
            inputLayout.addWidget(new_port)
            inputLayout.addStretch()

        bodyLayout = QHBoxLayout()
        bodyLayout.addWidget(QLabel(instName))
        
        outputLayout = QHBoxLayout()
        outputLayout.addStretch()
        for pout in outputPort:
            new_port = Port.PortOut(self)
            self.outPorts.append(new_port)
            outputLayout.addWidget(new_port)
            outputLayout.addStretch()

        layout.addLayout(outputLayout)
        layout.addWidget(QLabel(instName))
        layout.addWidget(QLabel('(%s)' % typeName))
        layout.addLayout(inputLayout)
        
        self.setLayout(layout)
        self.show()

    def mouseReleaseEvent(self, event):
        self.createPopupActions()
        self.createPopupMenu()

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData(self)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)

    def createPopupActions(self):
        menu_list = []
        self.setPopupActionList(menu_list)

    def createPopupMenu(self):
        """ This method creates popup menu and display on screen. Menu items will be given by child classes. Child classes must override createPopupActions to set menu items.
        """
        menu = QMenu()

        for action in self.popupActions:
            act = QAction(action["title"], self)
            act.setStatusTip(action["desc"])
            act.triggered.connect(action["method"])
            menu.addAction(act)

        menu.exec_(QCursor.pos())

    def setPopupActionList(self,menuList):
        for menu in menuList:
            if menu not in self.popupActions:
                self.popupActions.append(menu) 

    def checkPosition(self,pos):
        if pos.x() < self.pos().x():
            return False
        if pos.x() > self.pos().x() + self.width():
            return False
        if pos.y() < self.pos().y():
            return False
        if pos.y() > self.pos().y() + self.height():
            return False

        return True

    def isConnecting(self,pos):
        for port in self.outPorts:
            if port.checkPosition(pos-self.pos()):
                return port
        return None

    def isArrived(self,pos):
        for port in self.inPorts:
            if port.checkPosition(pos-self.pos()):
                return port
        return None

    def updatePortPos(self):
        for port in self.outPorts:
            if port.getConnection():
                port.getConnection().setSrcCoord(QPoint(port.pos().x()+port.width()/2,port.pos().y()+port.height()/2) + self.pos())

        for inport in self.inPorts:
            if inport.getConnection():
                inport.getConnection().setDstCoord(QPoint(inport.pos().x()+inport.width()/2,inport.pos().y()+inport.height()/2) + inport.parent.pos())

    def run(self):
        self.propagateExecution()
        self.execute()

    def execute(self):
        pass

    def propagateExecution(self):
        for port in self.inPorts:
            port.propagateExecution()
