# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from   PySide.QtCore import *
from   PySide.QtGui  import *
import time

class Ring(QGraphicsItem):
	def __init__(self, scene, x, y, w = 70, h = 70, status = 6,):
		QGraphicsItem.__init__(self, parent = None)
		self.color   = [QColor('#ff0043'), QColor('#ff6900'), QColor('#fbff00'), QColor('#48ff00'), QColor('#0092ff'), QColor('#a100ff'), QColor('#0b0b0b'), QColor('#dfdfdf'), QColor('#878787')]
		self.status  = status
		self.scene   = scene
		self.contentPos = QPoint(x-2,y-2)
		self.setFlag(QGraphicsItem.ItemIsMovable)
 
		self.w = w
		self.h = h

	def setStatus(self, status):
		self.status = status 
		self.update()  

	def getStatus(self):
		return self.status

	def paint(self, painter, option, widget):

		painter.setPen(QPen(self.color[self.status], 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))   
		painter.setRenderHint(QPainter.Antialiasing)

		painter.drawEllipse(self.contentPos.x()  , self.contentPos.y() , 68, 68)

	def mousePressEvent(self, event):
		event.ignore() 

	def contentSceneRect(self):
		return QRect(int(self.contentPos.x()), int(self.contentPos.y()), self.w, self.h)
	
	def contentSceneRectF(self):
		return QRectF(self.contentPos, QSize(self.w, self.h))    
	
	def contentRect(self):
		return self.mapToItem(self, self.contentSceneRect()).boundingRect()
		
	def boundingRect(self):          
		boundingRect = self.contentSceneRectF()
		return boundingRect   
