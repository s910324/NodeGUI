# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
from PySide.QtCore import *
from PySide.QtGui import *
from PysideGraph import *
from ScriptNode import *


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.view  = QGraphicsView()
		self.scene = QGraphicsScene()
		self.scene.setSceneRect(0,0,800,600)
		self.setCentralWidget(self.view)
		#Select node connection and its decorator types
		self.nc = CenterCalc()
		self.cd = LineArrowOnStart()          

		#make root node and add it to the scene
		root = ImageNode(self.nc, self.cd, None, "root", QImage("./img/0m071d022a7251e689c7664af712182c8c52ad34200b73.png"), 400, 20, 64,64 )

		self.scene.addItem(root)

		#create graph nodes
		a = TextNode(self.nc, self.cd, root, "node", "Node" , 500, 340, 200, 30)
		root.addChild( a)
		scn = ScriptNode(self.nc, self.cd, root, "node", "Node" , 500, 340, 200, 30)

		scn.changeScript(self.a, ['2234'])
		root.addChild(scn)  

		scn.runScript()
		self.view.setScene(self.scene)
		self.view.show()

	def runSceneScripts(self):
		print 'a'
	def a(self,b):
		print str(b)		
app = QApplication(sys.argv)
# MainWindow = listItem()
MainWindow = MainWindow()
MainWindow.show()
def load_stylesheet(pyside=True):
	f = QFile("./style.qss")
	if not f.exists():
		return ""
	else:
		f.open(QFile.ReadOnly | QFile.Text)
		ts = QTextStream(f)
		stylesheet = ts.readAll()
		return stylesheet	
app.setStyleSheet(load_stylesheet())
app.exec_()
