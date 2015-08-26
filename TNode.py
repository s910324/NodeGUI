# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from   TextNode      import *
from   PySide.QtCore import *
from   PySide.QtGui  import *

class TNode(QGraphicsItem):
	def __init__(self, scene, text, x, y, w, h):
		QGraphicsItem.__init__(self)	
		self.text       = text
		self.scene      = scene
		self.contentPos = QPoint(x,y)
		self.setFlag(QGraphicsItem.ItemIsMovable)

		self.w = w
		self.h = h


 
	def contentSceneRect(self):
		return QRect(int(self.contentPos.x()), int(self.contentPos.y()), self.w, self.h)
	
	def contentSceneRectF(self):
		return QRectF(self.contentPos, QSize(self.w, self.h))    
	
	def contentRect(self):
		return self.mapToItem(self, self.contentSceneRect()).boundingRect()
		
	def boundingRect(self):          
		boundingRect = self.contentSceneRectF()
		return boundingRect   
