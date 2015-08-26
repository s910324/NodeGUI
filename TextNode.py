# -*- coding: utf-8 -*-
from __future__    import unicode_literals
from TNode         import TNode
from PySide.QtCore import *
from PySide.QtGui  import *

class TextNode(TNode):
	def __init__(self, scene, text = '', x = 0, y = 0, w = 100, h = 20, size = 10, bold = True,  align = 'left'):
		TNode.__init__(self, scene, text, x, y, w, h) 
		self.text  = text
		self.size  = size
		self.scene = scene
		if bold is True:
			self.font = QFont.Bold
		else:
			self.font = QFont.Normal

		if   align == 'left':
			self.align = Qt.AlignLeft
		elif align == 'right':
			self.align = Qt.AlignRight
		elif align == 'center':
			self.align = Qt.AlignCenter

	def changeText(self, text, size = 10, bold = True, align = 'left'):
		self.text = text
		self.size = size
		if bold is True:
			self.font = QFont.Bold
		else:
			self.font = QFont.Normal

		if   align == 'left':
			self.align = Qt.AlignLeft
		elif align == 'right':
			self.align = Qt.AlignRight
		elif align == 'center':
			self.align = Qt.AlignCenter
		self.update()       
	def selfDestory(self):
		self.scene.removeItem(self)
		del self

	def paint(self, painter, option, widget):
		painter.setFont(QFont('Decorative', self.size, self.font))
		painter.drawText(self.contentRect(), self.align, self.text)

	def mousePressEvent(self, event):
		event.ignore() 