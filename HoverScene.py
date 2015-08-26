# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from   PySide.QtCore import *
from   PySide.QtGui  import *
from   PysideGraph   import *
class DiagramScene(QGraphicsScene):
	def __init__(self, parent=None):
		super(DiagramScene, self).__init__(parent)
		self.lineColor = QColor('#202020')
		self.drawBG()
		self.JNodes = []

	def drawBG(self):
		res = 1920
		for i in xrange(-res,res,50):
			self.addLine(i,-res,i,res, QPen(self.lineColor))
			self.addLine(-res,i,res,i, QPen(self.lineColor))

	def runScript(self):
		runSequence = []
		for JNode in self.JNodes:
			# which node is not root node, which should initiallize it parameters
			JNode.setStatus(0)
			if JNode.getHost() == []:
				runSequence.append(JNode)
			else:
				JNode.clear()

		for JNode in runSequence:
			runSequence += JNode.client
		for JNode in runSequence:
			if JNode in runSequence[runSequence.index(JNode)+1:]:
				runSequence.pop(runSequence.index(JNode))

		for JNode in runSequence:
			try:
				JNode.runScript()
			# except Exception:
			# 	print u"function executed with error value"
			# 	break
			except NameError:
				print 'abs'
			except TypeError:
				pass
				
		for unExecuted in self.JNodes:
			if unExecuted not in runSequence:
				unExecuted.setStatus(0)
