# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from   types         import *
from   PlugNode      import *
from   TextNode      import *
from   LineCalc      import *
from   LineDecorator import *
from   PySide.QtCore import *
from   PySide.QtGui  import *

class SNode(QGraphicsItem):
	def __init__(self, scene, lineCalc, lineDecorator, parent, x, y, w, h, name = None):
		QGraphicsItem.__init__(self, parent)
		
		self.lineCalc      = lineCalc
		self.lineDecorator = lineDecorator
		self.nameTag = TextNode(self.scene, text = name, x = x-105, y= y-3)
		self.name    = name
		self.parent  = parent
		self.host    = None
		self.scene   = scene
		self.child   = []


		#in screen coords
		self.contentPos = QPoint(x,y) #self.scenePos()
		self.setFlag(QGraphicsItem.ItemIsMovable)
		self.setAcceptHoverEvents(True)
			   
		#width and height of content (img, text) without the arrows
		self.w = w
		self.h = h

		#variables for proper dragging and scaling
		self.resizeMode = False
		self.moveMode   = False   
		self.ignore     = False   
		self.lineRect   = None
		self.setAcceptDrops(True)
		#bounding rectangle which encapsulates the arrow to parent
 
	def getName(self):
		return self.name

	def setName(self, name):
		self.name    = name
		self.nameTag.changeText(name, size = 8, bold = False, align = 'right')
	
	def setParent(self, parent):
		self.parent  = parent

	def setHost(self, host):
		self.host    = host
		if self.nameTag not in self.host.parts:
			self.scene.addItem(self.nameTag)
			self.host.parts.append(self.nameTag)

	def getHost(self):
		return self.host

	def setLevel(self, level):
		self.host.level = level

	def getLevel(self):
		return self.host.level

	def addChild(self, node):
		# kill PNode connections with others,
		# re-assign parent to self to establish connection.
		# node.killConnect()          node???
		node.killConnect()
		
		if node not in self.child:
			addCheck = self.getHost().addClient(node.getHost())
			if addCheck:
				self.child.append(node)
				node.setParent(self)


		
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
			self.coursor = [event.scenePos().x(), event.scenePos().y()]
			self.coursorLine = 0
		self.update()
			
	def mouseReleaseEvent(self, event):
		if self.ignore:

			event.ignore()
		if event.button() == Qt.RightButton:
			self.resizeMode = False      
		if event.button() == Qt.LeftButton:
			self.moveMode = False
			self.coursorLine = 1		
			for i in self.scene.items():
				if type(i) == PlugNode:
					[ ix,  iy ]  = [ event.scenePos().x(),   event.scenePos().y() ]
					[ x,y,h,w ]  = [ i.contentPos.x(), i.contentPos.y(), i.h, i.w ]
					if (x <= ix <= x+w) and (y <= iy <= y+h):
						if self.getHost() is not i.getHost():
							self.addChild(i)
		self.update()

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
		
		if self.moveMode:    
			# move only the content, arrow will be redrawn
			self.prepareGeometryChange()
			p = event.scenePos() - self.offset
			self.contentPos = p

		self.coursor = [event.scenePos().x(), event.scenePos().y()]
		self.coursorLine = 0
		self.update()

# ----------------------------------

	def binomial(self, i, n):
		"""Binomial coefficient"""
		return math.factorial(n) / float(
			math.factorial(i) * math.factorial(n - i))


	def bernstein(self, t, i, n):
		"""Bernstein polynom"""
		return self.binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


	def bezier(self, t, points):
		"""Calculate coordinate of a point in the bezier curve"""
		n = len(points) - 1
		x = y = 0
		for i, pos in enumerate(points):
			bern = self.bernstein(t, i, n)
			x += pos[0] * bern
			y += pos[1] * bern
		return x, y


	def bezier_curve_range(self, n, points):
		"""Range of points in a curve bezier"""
		for i in xrange(n):
			t = i / float(n - 1)
			yield self.bezier(t, points)
		
	def drawRect(self, painter, rect):
		painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))   
		# painter.drawRect(rect)
		
	#draw line and decorators and recalculates bounding box
	def drawLine(self, painter, sourceRect, destRect):
		""" method for drawing line and decorators connecting parent and child node,
		recalculates also the line bounding box, which is used in node bounding box """
		self.prepareGeometryChange()
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(QPen(Qt.black, 2, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin))

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
		# sp = sourcePoint.toTuple()
		# dp = destPoint.toTuple()
		# qm = ((sourcePoint + destPoint)/2 +sourcePoint)/2
		# qm += QPointF(0.0, 45.0)
		# qm = qm.toTuple()
		# tm = ((sourcePoint + destPoint)/2 + destPoint)/2
		# tm -= QPointF(0.0, 45.0)
		# tm = tm.toTuple()

		# controlPoints = (sp, qm, tm, dp)
		# for point in self.bezier_curve_range(1000, controlPoints):
		# 	painter.drawLine(sp[0], sp[1], point[0], point[1])
		# 	sp = point



		decorators = self.lineDecorator.calcDecorator(line)
		painter.setBrush(Qt.black)
		
		for polygon in decorators:
			painter.drawPolygon(polygon)
			self.lineRect.united(polygon.boundingRect())
		return line

	#draw line and decorators and recalculates bounding box


