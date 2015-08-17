# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import threading
from   PySide.QtCore import *
from   PySide.QtGui  import *
from   JNode         import JNode


class JackNode(JNode):
    def __init__(self, scene, lineCalc, lineDecorator, parent = None, img = QImage("./img/a.png"), x = 0, y = 0, w = 64, h = 64, name = None):
        JNode.__init__(self, scene, lineCalc, lineDecorator, parent, x, y, w, h, name)    
        scene.addItem(self)
        scene.JNodes.append(self)
        self.img = img    
        if img is not None and (img.width() != self.w or img.height() != self.h):
            self.img = img.scaled(self.w, self.h)
        
        self.bitmap_lock = threading.Lock()
               
    def paint(self, painter, option, widget):

        if self.img    is not None:
            with self.bitmap_lock:
                painter.drawImage(self.contentRect(), self.img) 
            
        if self.parent is not None:
            self.drawLine(painter, self.contentSceneRect(), self.parent.contentSceneRect())     

        if self.name   is not None:
            pass

    def changeImg(self, img):        
        if img.width() != self.w or img.height() != self.h:
            img = img.scaled(self.w, self.h)
        
        with self.bitmap_lock:
            self.img = img            
        #self.update(self.contentSceneRect()) 
                   