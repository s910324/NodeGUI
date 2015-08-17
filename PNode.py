# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from   types         import *
from   LineCalc      import *
from   LineDecorator import *
from   PySide.QtCore import *
from   PySide.QtGui  import *

class PNode(QGraphicsItem):
	def __init__(self, scene, lineCalc, lineDecorator, parent, x, y, w, h, name = None):
		QGraphicsItem.__init__(self, parent)
		
		self.lineCalc      = lineCalc
		self.lineDecorator = lineDecorator
		self.name    = name
		self.parent  = parent
		self.host    = None
		self.child   = []
		self.level   = 0

		#in screen coords
		self.contentPos = QPoint(x,y) #self.scenePos()
		self.setFlag(QGraphicsItem.ItemIsMovable)
		self.setAcceptHoverEvents(True)

		#width and height of content (img, text) without the arrows
		self.w = w
		self.h = h

		#variables for proper dragging and scaling
		self.resizeMode  = False
		self.moveMode    = False
		self.connectMode = False 
		self.ignore      = False   
		self.lineRect    = None  
		#bounding rectangle which encapsulates the arrow to parent
 
	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name
	
	def setParent(self, parent):
		self.parent = parent

	def setHost(self, host):
		self.host = host

	def getHost(self):
		return self.host

	def setLevel(self, level):
		self.host.level = level	

	def getLevel(self):
		return self.host.level

	def addChild(self, node):
		# useless in this node, connection is establish from source node.
		# set connection to source Nodes.
		# not currently in use, connection should be establish from source.

		if node not in self.child:
			self.child.append(node)
			node.setParent(self)


	def killConnect(self):
		# self have connect, remove self from parent(sourceNode).child list
		# remove self.JackNode from  host.JackNode
		# and removeconnect(setParent as None).

		if self.parent is not None and self in self.parent.child:
			self_JackNode   = self.getHost()
			parent_JackNode = self.parent.getHost()

			self.parent.child.remove(self)

			parent_JackNode.removeClient(self_JackNode)
			self_JackNode.removeHost(parent_JackNode)
			self.setParent(None)


	def SetX(self,x):
		self.prepareGeometryChange()
		self.contentPos.setX(x)        
		
	def GetX(self):
		return self.contentPos.x()
	
	def SetY(self,y):
		self.prepareGeometryChange()
		self.contentPos.setY(y)     
	
	def GetY(self):
		return self.contentPos.y()
	
	def GetWidth(self):
		return self.w
	
	def SetWidth(self,w):
		self.prepareGeometryChange()
		self.w = w    
	
	def GetHeight(self):
		return self.h
	
	def SetHeight(self,h):
		self.prepareGeometryChange()
		self.h = h     
			   
	def contentSceneRect(self):
		return QRect(int(self.contentPos.x()), int(self.contentPos.y()), self.w, self.h)
	
	def contentSceneRectF(self):
		return QRectF(self.contentPos, QSize(self.w, self.h))    
	
	def contentRect(self):
		return self.mapToItem(self, self.contentSceneRect()).boundingRect()
		
	def boundingRect(self):
		"""important method for proper redrawing and not leaving artefacts"""              
		boundingRect = self.contentSceneRectF()
		   
		# include also bounding rectangle of arrows
		if self.lineRect is not None:
			boundingRect = boundingRect.united(self.lineRect)        
		
		for w in self.child :
			if w.lineRect is not None:
				boundingRect = boundingRect.united(w.lineRect)
					 
		return boundingRect   
	
	def mousePressEvent(self, event):
		# do not react on events on arrows
		rect = self.contentSceneRect()
		if not rect.contains(int(event.scenePos().x()), int(event.scenePos().y())):
			#ungrab mouse
			event.ignore()
			self.ignore = True
			return
				
		self.ignore = False
		if event.button() == Qt.RightButton:
			self.resizeMode = False
		if event.button() == Qt.LeftButton:
			self.moveMode = False

			
	def mouseReleaseEvent(self, event):
		if self.ignore:
			event.ignore()
		if event.button() == Qt.RightButton:
			self.resizeMode = False      
		if event.button() == Qt.LeftButton:
			self.moveMode = False    


	def mouseMoveEvent(self, event):          
		if self.ignore:
			event.ignore()        
		# calculate in screen coords (item coords is jerky, even.pos())
		if self.resizeMode:
			self.prepareGeometryChange()
			p = event.scenePos() - self.contentPos
			scalex = p.x()/self.w
			scaley = p.y()/self.h
			#rescale only the content, not arrow
			self.w = scalex * self.w
			self.h = scaley * self.h  
			self.update()
			
		if self.moveMode:    
			# move only the content, arrow will be redrawn
			self.prepareGeometryChange()
			p = event.scenePos() - self.offset
			self.contentPos = p
			self.update()




	def mouseDoubleClickEvent(self, event):
		self.killConnect()



			
	def drawRect(self, painter, rect):
		painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))   
		# painter.drawRect(rect)
		
	#draw line and decorators and recalculates bounding box
	def drawLine(self, painter, sourceRect, destRect):
		""" method for drawing line and decorators connecting parent and child node,
		recalculates also the line bounding box, which is used in node bounding box """
		self.prepareGeometryChange()
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

		(sourcePoint, destPoint) = self.lineCalc.calcEndPoints(sourceRect, destRect)
		#drawing in item coordinates
		sourcePoint   = self.mapToItem(self, sourcePoint)
		destPoint     = self.mapToItem(self, destPoint)    
		self.lineRect = QRectF(sourcePoint, destPoint)
		line          = QLineF(sourcePoint, destPoint)
		#nothing to draw
		if line.length() == 0:
			return
		painter.drawLine(line)
		
		decorators = self.lineDecorator.calcDecorator(line)
		painter.setBrush(Qt.black)
		
		for polygon in decorators:
			painter.drawPolygon(polygon)
			self.lineRect.united(polygon.boundingRect())  

	#draw line and decorators and recalculates bounding box


