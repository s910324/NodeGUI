# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from   PySide.QtCore import *
from   PySide.QtGui  import *
from   PysideGraph   import *
class DiagramScene(QGraphicsScene):
	def __init__(self, parent=None):
		super(DiagramScene, self).__init__(parent)
		self.drawBG()
		self.JNodes = []

	def drawBG(self):
		brush = QBrush(QColor('#202020'))
		brush.setStyle(Qt.CrossPattern)
		self.setBackgroundBrush(brush)

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
