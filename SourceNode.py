# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import threading
from   PySide.QtCore import *
from   PySide.QtGui  import *
from   SNode         import SNode

class SourceNode(SNode):

    def __init__(self, scene, lineCalc, lineDecorator, parent = None, img = QImage("./img/NodeRG.png"), x = 0, y = 0, w = 32, h = 10, name = None):
        SNode.__init__(self, scene, lineCalc, lineDecorator, parent, x, y, w, h, name)    
        self.coursorLine = 1
        self.coursor     = [0,0]
        self.img = img    
        if img is not None and (img.width() != self.w or img.height() != self.h):
            self.img = img.scaled(self.w, self.h)
        
        self.bitmap_lock = threading.Lock()
               
    def paint(self, painter, option, widget):
        #Local coords !!
        self.drawRect(painter, self.contentRect())  

        if self.img is not None:
            with self.bitmap_lock:
                painter.drawImage(self.contentRect(), self.img) 
            
        if self.parent is not None:
            self.drawLine(painter, self.contentSceneRect(), self.parent.contentSceneRect())     

        if self.coursorLine is 0:
            self.drawLine(painter, QRect(self.coursor[0], self.coursor[1],10,10), self.contentSceneRect()  ) 
 
    def changeImg(self, img):        
        if img.width() != self.w or img.height() != self.h:
            img = img.scaled(self.w, self.h)
        
        with self.bitmap_lock:
            self.img = img            
        #self.update(self.contentSceneRect()) 
              