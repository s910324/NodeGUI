# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import threading

from   types         import *
from   PySide.QtCore import *
from   PySide.QtGui  import *
from   PNode         import PNode

class PlugNode(PNode):
	def __init__(self, scene, lineCalc, lineDecorator, parent = None, img = QImage("./img/NodeG.png"), x = 0, y = 0, w = 10, h = 10, name = None):
		PNode.__init__(self, scene, lineCalc, lineDecorator, parent, x, y, w, h, name)  

		self.Pen   = [QPen(QColor('#0A0A0A'), 1, Qt.SolidLine),  #normal  state
					  QPen(QColor('#2A2A2A'), 1, Qt.SolidLine),  #hovered state
					  QPen(QColor('#0AFA0A'), 1, Qt.DashLine),   #ready to connect
					  QPen(QColor('#FF0A0A'), 2, Qt.SolidLine)]  #error   state  
		self.Brush = [QColor(255,  0, 118, 200),
					  QColor( 20, 20,  20, 255),
					  QColor( 28, 28,  28, 200),
					  QColor( 28, 28,  28, 200)]

		self.coursorLine = 1
		self.coursor     = [0,0]
		# self.img         = img 

		# if img is not None and (img.width() != self.w or img.height() != self.h):
		# 	self.img = img.scaled(self.w, self.h)

		# self.bitmap_lock = threading.Lock()
			   
	def paint(self, painter, option, widget):
		#Local coords !!
		painter.setRenderHint(QPainter.Antialiasing)    	
		painter.setPen(self.Pen[0])
		painter.setBrush(self.Brush[0])
		painter.drawEllipse (self.contentPos.x(), self.contentPos.y(), 8, 8)
		self.drawRect(painter, self.contentRect())  
		
		# if self.img is not None:
		# 	with self.bitmap_lock:
		# 		painter.drawImage(self.contentRect(), self.img) 



			
		if self.parent is not None:
			self.drawLine(painter, self.contentSceneRect(), self.parent.contentSceneRect())     

		if self.coursorLine is 0:
			self.drawLine(painter, self.contentSceneRect(), QRect(self.coursor[0], self.coursor[1],10,10)  ) 
		# self.update(self.contentSceneRect())


	def changeImg(self, img):        
		if img.width() != self.w or img.height() != self.h:
			img = img.scaled(self.w, self.h)
		
		with self.bitmap_lock:
			self.img = img            
	# 	self.update(self.contentSceneRect()) 

	
				   