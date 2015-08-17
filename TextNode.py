# -*- coding: utf-8 -*-
from __future__    import unicode_literals
from TNode         import TNode
from PySide.QtCore import *
from PySide.QtGui  import *

class TextNode(TNode):
	def __init__(self, scene, text = '', x = 0, y = 0, w = 100, h = 20):
		TNode.__init__(self, scene, text, x, y, w, h) 
		self.text = text
		
	def changeText(self, text):
		self.text = text 
		self.update()       
		
	def paint(self, painter, option, widget):
		painter.setFont(QFont('Decorative', 10, QFont.Bold))
		painter.drawText(self.contentRect(), Qt.AlignCenter, self.text)

	def mousePressEvent(self, event):
		event.ignore() 