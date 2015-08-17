'''
Created on Oct 19, 2011

@author: htruskova
'''
from Node import Node

class ScriptNode(Node):
    def __init__(self, lineCalc, lineDecorator, parent, name, text = " ", x = 0, y = 0, w = 100, h = 100):
        Node.__init__(self, lineCalc, lineDecorator, parent, name, x, y, w, h) 
        self.text       = text
        self.script     = None
        self.parameters = []
    def changeText(self, text):
        self.text = text        
        
    def paint(self, painter, option, widget):
        painter.drawText(self.contentRect(), self.text)   
        
        self.drawRect(painter, self.contentRect())  
            
        if self.parent is not None:
            self.drawLine(painter, self.contentSceneRect(), self.parent.contentSceneRect()) 

    def changeScript(self, script, parameters = []):
        self.script     = script
        self.parameters = parameters

    def runScript(self):
        if self.script != None:
            if len(self.parameters ) != 0:
                self.script(*self.parameters)
            else:
                self.script()

    def type(self):
        return '<ScriptNode>'