import numpy as np
import matplotlib.pyplot as plt
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox

class Box(CommonModuleBox):
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = ''):
        self.typeName = type(self)
        super().__init__(parent, inputPort, outputPort, instName, self.typeName)

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Export", "desc":"Export logic to source code", "method":self.export},
                 {"title":"Train", "desc":"Train", "method":self.train},
                 {"title":"Config", "desc":"Configure module parameters", "method":self.config},
                 {"title":"Run", "desc":"Configure module parameters", "method":self.run}]
        self.setPopupActionList(menus)

    def export(self):
        pass

    def train(self):
        pass

    def config(self):
        pass

    def execute(self):
        for pin in self.inPorts:
            data = pin.getData()

        fig = plt.figure()
        ax = fig.subplots()
        ax.scatter(data[:,0],data[:,1])
        plt.show()
