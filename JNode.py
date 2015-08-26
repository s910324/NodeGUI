# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from   LineCalc      import *
from   LineDecorator import *
from   PlugNode      import *
from   SourceNode    import *
from   TextNode      import *
from   Ring          import *
from   PySide.QtCore import *
from   PySide.QtGui  import *
from   ErrorClass    import *

class JNode(QGraphicsItem):
	def __init__(self, scene, lineCalc, lineDecorator, parent,  x , y, w , h, name = None):
		QGraphicsItem.__init__(self, parent)
		
		self.Pcount         = 0
		self.Scount         = 0
		self.scene          = scene
		self.lineCalc       = lineCalc
		self.lineDecorator  = lineDecorator
		self.nameTag        = TextNode(self.scene, text = name, x= x+10, y= y+5)
		self.nameTag.changeText(name)
		

		self.name       = name
		self.parent     = parent
		self.status     = 0
		self.temp_stat  = 0
		self.host       = []
		self.client     = []
		self.child      = []
		self.jack       = []
		self.drain      = []
		self.parts      = [self.nameTag]  #self.Ring,
		self.level      = None

		self.script     = None
		# self.parameters = None
		self.output     = TypeError

		self.contentPos = QPoint(x,y) #self.scenePos()
		self.setFlag(QGraphicsItem.ItemIsMovable)
		self.setAcceptHoverEvents(True)
		self.setLevel(-1)

		#width and height of content (img, text) without the arrows
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		#variables for proper dragging and scaling
		self.resizeMode = False
		self.moveMode   = False   
		self.ignore     = False   
		self.lineRect   = None  
		#bounding rectangle which encapsulates the arrow to parent

	def source(self, num):
		return self.drain[num]

	def plug(self, num):
		return self.jack[num] 	

	def setName(self, name):
		self.name = name
		self.nameTag.changeText(name)

	def getName(self):
		return self.name

	def setLevel(self, level):
		self.level = level

	def getLevel(self):
		return self.level

	def setStatus(self, status):
		self.status = status

	def getStatus(self):
		return self.status

	def addChild(self, node):
		self.child.append(node)

	def addHost(self, hostJack):
		if hostJack not in self.host:
			self.host.append(hostJack)
	
	def getHost(self):
		return self.host

	def removeHost(self, hostJack):
		self.setStatus(0)
		if hostJack in self.host:
			self.host.remove(hostJack)

	def setScript(self, script, parameters = []):
		self.script     = script
		self.parameters = parameters

	def runScript(self):
		if self.script != None:
			self.parameters = []
			for plug in self.jack: 
				if plug.parent == None:
					# not connected,use function defaults
					self.parameters.append(self.script.func_defaults[self.jack.index(plug)])
				elif (plug.parent.getHost().output) is TypeError:
					self.setStatus(3)
					raise TypeError
				else:

					self.parameters.append(plug.parent.getHost().output)
					# paremeters = [Jnode.output, ... ]

			if (self.parameters ) != None:
				self.output = self.script(*self.parameters)
			else:
				self.output = self.script()
			# if self.output != TypeError:
			# 	self.setName(str(self.output))

	def clear(self):
		self.output = TypeError

	def selfDestory(self):
		self.clear()
		self.nameTag.selfDestory()
		for plug in self.jack:
			plug.selfDestory()

		for source in self.drain:
			source.selfDestory()

		if self in self.scene.JNodes:
			self.scene.JNodes.pop(self.scene.JNodes.index(self))
			self.scene.removeItem(self)

		del self

	def addClient(self, clientJack):
		if clientJack not in self.client:
			clientJack.addHost(self)
			self.client.append(clientJack)
			# if clientJack.getLevel() <= self.getLevel():
		# 	clientJack.setLevel(clientJack.getLevel() + self.getLevel() + 1)
		# 	for c in clientJack.client:
		# 		if c not in self.client:
		# 			self.client.append(c)
		# 			for hostJack in self.host:
		# 				hostJack.addClient(c)
		# 			c.setLevel(c.getLevel() + self.getLevel() + 1)			
			return True
		# return False




	def removeClient(self, clientJack):
		
		if clientJack in self.client:
			self.client.remove(clientJack)
		# 	clientJack.setLevel(clientJack.getLevel() - self.getLevel() - 1)
		# for c in clientJack.client:
		# 	if c  in self.client:
		# 		self.client.remove(c)
		# 		c.setLevel(c.getLevel() - self.getLevel() - 1)		
		
	def addPlug(self, count = 1, name = "None"):
		if self.Pcount == 0:
			self.setLevel(0)
		for i in xrange(count):
			self.Pcount += 1
			plug = PlugNode(self.scene, self.lineCalc, self.lineDecorator, x= self.x +5, y= self.y + 20 + (15) * self.Pcount, name = name)
			plug.setName(name)
			plug.setHost(self)
			self.jack.append(plug)
			self.scene.addItem(plug)
		if (self.Pcount - self.Scount > 1) and (self.Pcount > 2) :
			self.SetHeight(self.GetHeight() + 15)

	def addSource(self, count = 1, name = "None"):
		for i in xrange(count):
			self.Scount += 1
			source = SourceNode(self.scene, self.lineCalc, self.lineDecorator, x= self.x + 85, y= self.y+30 + (15) * self.Scount, name = name)
			source.setName(name)
			source.setHost(self)
			self.drain.append(source)
			self.scene.addItem(source)

		if (self.Scount - self.Pcount >= 0 ) and (self.Scount > 1):
			self.SetHeight(self.GetHeight() + 15)

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
		if self.lineRect is not None:
			boundingRect = boundingRect.united(self.lineRect)        
		
		for w in self.child :
			if w.lineRect is not None:
				boundingRect = boundingRect.united(w.lineRect)
		return boundingRect   

	def hoverEnterEvent (self, event):
		event.accept()	
		self.temp_stat = self.status
		self.status = 1
		self.update()

	def hoverLeaveEvent (self, event):
		event.accept()	
		self.status = self.temp_stat
		self.update()		

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
			self.menu = QMenu()
			self.menu.addAction('[x] delete this Node', self.selfDestory)
			self.menu.addAction('[+] add input', self.addPlug)
			self.menu.popup(event.screenPos())
			
			# connect(menu, SIGNAL(triggered(QAction *)),object, SLOT(triggered(QAction *)))
			self.resizeMode = False
			

		if event.button() == Qt.LeftButton:
			self.moveMode = True  
			self.offset = event.scenePos() - self.contentPos
			for plug in self.jack:
				plug.moveMode = True  
				plug.offset = event.scenePos() - plug.contentPos
			for source in self.drain:
				source.moveMode = True  
				source.offset = event.scenePos() - source.contentPos	
			
			for part in self.parts:
				part.moveMode = True  
				part.offset = event.scenePos() - part.contentPos


	def mouseReleaseEvent(self, event):
		if self.ignore:
			event.ignore()
		if event.button() == Qt.RightButton:
			self.resizeMode = False      

		if event.button() == Qt.LeftButton:
			self.moveMode = False   
			for plug in self.jack:
				plug.moveMode = False
			for source in self.drain:
				source.moveMode = False
			for part in self.parts:
				part.moveMode = False


	def mouseMoveEvent(self, event):          
		if self.ignore:
			event.ignore()        
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
			for plug in self.jack:
				plug.prepareGeometryChange()
				p = event.scenePos() - plug.offset
				plug.contentPos = p
				plug.update()
			for source in self.drain:
				source.prepareGeometryChange()
				p = event.scenePos() - source.offset
				source.contentPos = p
				source.update()

			for part in self.parts:
				part.prepareGeometryChange()
				p = event.scenePos() - part.offset
				part.contentPos = p
				part.update()

	def drawRect(self, painter, rect):
		painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))   

	def drawLine(self, painter, sourceRect, destRect):
		""" method for drawing line and decorators connecting parent and child node,
		recalculates also the line bounding box, which is used in node bounding box """
		self.prepareGeometryChange()
		painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
		
		(sourcePoint, destPoint) = self.lineCalc.calcEndPoints(sourceRect, destRect)
		#drawing in item coordinates
		sourcePoint = self.mapToItem(self, sourcePoint)
		destPoint = self.mapToItem(self, destPoint)    
		
		self.lineRect = QRectF(sourcePoint, destPoint)
		line = QLineF(sourcePoint, destPoint)
		#nothing to draw
		if line.length() == 0:
			return
		painter.drawLine(line)
		
		decorators = self.lineDecorator.calcDecorator(line)
		painter.setBrush(Qt.black)
		
		for polygon in decorators:
			painter.drawPolygon(polygon)
			self.lineRect.united(polygon.boundingRect())   





