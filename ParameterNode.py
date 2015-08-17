'''
Created on Oct 19, 2011

@author: htruskova
'''
from Node import Node

class ParameterNode(Node):
    """\brief Graph node with text content """
    def __init__(self, lineCalc, lineDecorator, parent, name, text = " ", x = 0, y = 0, w = 100, h = 100):
        Node.__init__(self, lineCalc, lineDecorator, parent, name, x, y, w, h) 
        self.text = text
        self.parameters = []
        
    def changeText(self, text):
        self.text = text        
        
    def paint(self, painter, option, widget):
        painter.drawText(self.contentRect(), self.text)   
        
        self.drawRect(painter, self.contentRect())  
            
        if self.parent is not None:
            self.drawLine(painter, self.contentSceneRect(), self.parent.contentSceneRect()) 
            
    def setValues(self, parameters):
        self.parameters = parameters

    def pushValues(self):
        return self.parameters

    def type(self):
        return '<ParameterNode>'            